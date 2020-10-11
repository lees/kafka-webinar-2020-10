CREATE TABLE db1.queue (
  ts DateTime,
  user_id UInt32,
  geo String,
  object_id String,
  domain String,
  url String,
  url_from String
) ENGINE = Kafka
SETTINGS kafka_broker_list = 'rc1a-3ni42npc97tl05t7.mdb.yandexcloud.net:9092',
         kafka_topic_list = 'test-topic',
         kafka_group_name = 'queue',
         kafka_format = 'JSONEachRow',
         kafka_skip_broken_messages = 1,
         kafka_num_consumers = 1,
         kafka_max_block_size = 1048576;

CREATE TABLE db1.events (
  ts DateTime,
  user_id UInt32,
  geo String,
  object_id String,
  domain String,
  url String,
  url_from String
) ENGINE = MergeTree
PARTITION BY toYYYYMM(ts)
ORDER BY (ts);

CREATE MATERIALIZED VIEW db1.events_mv TO db1.events AS SELECT * FROM db1.queue;