import json
import random
import time
import uuid
from datetime import datetime

from confluent_kafka import Producer

from common.geohash_utils import generate_random_geohash, get_sleep_interval
from common.kafka_config import KAFKA_CONFIG

producer = Producer(KAFKA_CONFIG)

STATUSES = ["AVAILABLE", "ON_TRIP"]

print("Driver Producer Started...")

while True:
    geohash = generate_random_geohash()
    hour = datetime.now().hour
    is_peak = 7 <= hour <= 10 or 17 <= hour <= 21

    driver_event = {
        "driver_id": str(uuid.uuid4()),
        "geohash": geohash,
        "status": random.choices(
            STATUSES, weights=[0.7, 0.3] if is_peak else [0.5, 0.5], k=1
        )[0],
        "rating": round(random.uniform(3.5, 5.0), 2),
        "event_time": int(time.time() * 1000),
        "is_peak": is_peak,
    }

    producer.produce(
        "driver_locations",
        key=geohash.encode("utf-8"),
        value=json.dumps(driver_event).encode("utf-8"),
    )
    producer.flush()

    print("DRIVER EVENT:", driver_event)
    time.sleep(get_sleep_interval())
