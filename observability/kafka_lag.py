from confluent_kafka import Consumer, TopicPartition


def get_topic_lag(topic, broker, group_id):
    consumer = Consumer(
        {
            "bootstrap.servers": broker,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        }
    )

    try:
        metadata = consumer.list_topics(topic=topic, timeout=10)
        if topic not in metadata.topics:
            return []

        lag_data = []
        for p_id in metadata.topics[topic].partitions.keys():
            tp = TopicPartition(topic, p_id)
            low, high = consumer.get_watermark_offsets(tp, timeout=10)
            committed = consumer.committed([tp], timeout=10)[0]
            committed_offset = (
                committed.offset if committed and committed.offset >= 0 else 0
            )
            lag_data.append(
                {
                    "partition": p_id,
                    "committed_offset": committed_offset,
                    "end_offset": high,
                    "lag": max(0, high - committed_offset),
                }
            )
        return lag_data
    finally:
        consumer.close()
