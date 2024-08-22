from kafka import KafkaProducer
import json
from data import get_registered_user
import time


def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def get_partition(key, all, available):
    return 1



producer = KafkaProducer(
    bootstrap_servers=['0.0.0.0:9092'],
    value_serializer=json_serializer,
    partitioner=get_partition
)


if __name__ == '__main__':
    while True:
        registred_user = get_registered_user()
        #print(registred_user)
        producer.send('foobar', registred_user)
        time.sleep(4)