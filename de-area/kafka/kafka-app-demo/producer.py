import time
import json
from kafka import KafkaProducer
from faker import Faker


fake = Faker()


def get_registered_user():
    
    return {
        'name': fake.name(),
        'address': fake.address(),
        'created_at': fake.year()
    }


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


producer = KafkaProducer(
    bootstrap_servers=['0.0.0.0:9092'],
    value_serializer=json_serializer
)


if __name__ == '__main__':
    while True:
        producer.send('reg_user', get_registered_user())
        time.sleep(3)