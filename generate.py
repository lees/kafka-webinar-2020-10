import time
import random
import socket
from datetime import datetime
import json

from confluent_kafka import Producer

def error_callback(err):
    print('Something went wrong: {}'.format(err))


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered ' + str(msg))

servers = "broker-fqdn:9091"

params = {
    'bootstrap.servers': servers,
    'request.timeout.ms': 10 * 1000,
    'security.protocol': 'SASL_SSL',
    'ssl.ca.location': '/usr/local/share/ca-certificates/Yandex/YandexCA.crt',
    'sasl.mechanism': 'SCRAM-SHA-512',
    'sasl.username': 'producer',
    'sasl.password': 'ProducerPassword',
    'error_cb': error_callback,
}

p = Producer(params)
p.poll(0)
for i in range(100):
    object_type = random.choice(['banner', 'article', 'link'])
    object_id = str( random.randint(1,30))
    data = {
        'ts': int(time.time()),
        'user_id': random.randint(1,30),
        'geo': random.choice(['ru', 'ua', 'kz']),
        'object_id': f'{object_type}{object_id}',
        'domain': 'example.com',
        'url': f'https://example.com/{object_type}/{object_id}',
        'url_from': 'https://example.com/',
    }
    p.produce('test-topic', json.dumps(data), key=str(data['user_id']), callback=delivery_report)
p.flush(10)