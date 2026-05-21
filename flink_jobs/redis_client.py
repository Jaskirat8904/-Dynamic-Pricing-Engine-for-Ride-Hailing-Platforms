import json

import redis

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


def get_alpha():

    config = redis_client.get("surge_config")

    if config:
        return json.loads(config)

    return {"default_alpha": 1.5}
