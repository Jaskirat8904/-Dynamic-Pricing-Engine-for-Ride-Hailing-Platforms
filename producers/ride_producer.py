import json
import random
import time
import uuid
from datetime import datetime

from confluent_kafka import Producer

from common.geohash_utils import generate_random_geohash, get_sleep_interval
from common.kafka_config import KAFKA_CONFIG

producer = Producer(KAFKA_CONFIG)

print("Ride Producer Started...")

while True:
    geohash = generate_random_geohash()
    hour = datetime.now().hour
    is_peak = 7 <= hour <= 10 or 17 <= hour <= 21

    ride_event = {
        "event_id": str(uuid.uuid4()),
        "rider_id": str(uuid.uuid4()),
        "geohash": geohash,
        "event_time": int(time.time() * 1000),
        "base_price": random.randint(100, 500),
        "ride_type": random.choice(["MINI", "SEDAN", "SUV"]),
        "is_peak": is_peak,
    }

    producer.produce(
        "ride_requests",
        key=geohash.encode("utf-8"),
        value=json.dumps(ride_event).encode("utf-8"),
    )
    producer.flush()

    print("RIDE EVENT:", ride_event)
    time.sleep(get_sleep_interval())
