from kafka import KafkaConsumer
import json 


if __name__ == '__main__':
    consumer = KafkaConsumer(
        'reg_user',
        bootstrap_servers='0.0.0.0:9092',
        auto_offset_reset='earliest',
        group_id='consumer-group-a'
    )
    print('Starting the consumer')
    for m in consumer:
        print(f'Registered User: {json.loads(m.value)}') 