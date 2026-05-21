import json
import time
from collections import defaultdict, deque
from datetime import datetime

import redis
from confluent_kafka import Consumer, Producer

from storage.save_record import save_pricing_window

KAFKA_BROKER = "localhost:9092"
WINDOW_DURATION = 60
SMOOTHING_WINDOW = 5

ride_consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "surge-engine-rides",
        "auto.offset.reset": "earliest",
    }
)

driver_consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "surge-engine-drivers",
        "auto.offset.reset": "earliest",
    }
)

ride_consumer.subscribe(["ride_requests"])
driver_consumer.subscribe(["driver_locations"])

producer = Producer({"bootstrap.servers": KAFKA_BROKER})
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

ride_counts = defaultdict(int)
driver_counts = defaultdict(int)
ride_history = defaultdict(lambda: deque(maxlen=SMOOTHING_WINDOW))
driver_history = defaultdict(lambda: deque(maxlen=SMOOTHING_WINDOW))
last_emit_time = time.time()


def peak_hour_multiplier():
    hour = datetime.now().hour
    if 7 <= hour <= 10:
        return 1.20
    if 17 <= hour <= 21:
        return 1.30
    return 1.0


def compute_surge(demand, supply, alpha):
    demand = max(demand, 0)
    supply = max(supply, 1)
    ratio = demand / supply
    smoothed = 0.7 * ratio + 0.3 * alpha
    surge = smoothed * peak_hour_multiplier()
    return round(min(5.0, max(1.0, surge)), 2)


print("Real-Time Surge Engine Started...")
print(f"Window duration: {WINDOW_DURATION}s")

while True:
    ride_msg = ride_consumer.poll(0.05)
    if ride_msg is not None and not ride_msg.error():
        try:
            ride_data = json.loads(ride_msg.value().decode("utf-8"))
            geohash = ride_data.get("geohash")
            if geohash:
                ride_counts[geohash] += 1
        except:
            pass

    driver_msg = driver_consumer.poll(0.05)
    if driver_msg is not None and not driver_msg.error():
        try:
            driver_data = json.loads(driver_msg.value().decode("utf-8"))
            if driver_data.get("status") == "AVAILABLE":
                geohash = driver_data.get("geohash")
                if geohash:
                    driver_counts[geohash] += 1
        except:
            pass

    current_time = time.time()

    if current_time - last_emit_time >= WINDOW_DURATION:
        old_ride_counts = ride_counts
        old_driver_counts = driver_counts
        ride_counts = defaultdict(int)
        driver_counts = defaultdict(int)
        last_emit_time = current_time

        all_geohashes = set(old_ride_counts.keys()) | set(old_driver_counts.keys())

        print("\n========== SURGE WINDOW ==========\n")

        for geohash in all_geohashes:
            demand = old_ride_counts.get(geohash, 0)
            supply = old_driver_counts.get(geohash, 1)

            ride_history[geohash].append(demand)
            driver_history[geohash].append(supply)

            avg_demand = sum(ride_history[geohash]) / len(ride_history[geohash])
            avg_supply = sum(driver_history[geohash]) / len(driver_history[geohash])

            alpha = float(
                r.get(f"surge_alpha:{geohash}")
                or r.get("optimal_alpha")
                or r.get("default_alpha")
                or 1.5
            )

            surge_multiplier = compute_surge(avg_demand, avg_supply, alpha)

            base_fares = json.loads(
                r.get("base_fares") or '{"MINI": 80, "SEDAN": 120, "SUV": 200}'
            )
            base_fare = base_fares.get("MINI", 80)
            final_min = round(base_fare * surge_multiplier * 0.9)
            final_max = round(base_fare * surge_multiplier * 1.1)

            output_event = {
                "geohash": geohash,
                "demand": demand,
                "supply": supply,
                "avg_demand": round(avg_demand, 2),
                "avg_supply": round(avg_supply, 2),
                "alpha": round(alpha, 2),
                "peak_hour_multiplier": peak_hour_multiplier(),
                "surge_multiplier": surge_multiplier,
                "final_price_range": f"Rs.{final_min} - Rs.{final_max}",
                "window_timestamp": int(time.time()),
            }

            r.setex(f"surge:{geohash}", WINDOW_DURATION * 2, str(surge_multiplier))
            r.set(f"latest_window:{geohash}", json.dumps(output_event))
            r.rpush(
                f"surge_history:{geohash}",
                json.dumps({"ts": int(time.time()), "surge": surge_multiplier}),
            )
            r.ltrim(f"surge_history:{geohash}", -2880, -1)

            save_pricing_window(output_event)

            producer.produce(
                "calculated_surge",
                key=geohash.encode("utf-8"),
                value=json.dumps(output_event).encode("utf-8"),
            )

            print(output_event)

        producer.flush()
        print("\n===================================\n")
