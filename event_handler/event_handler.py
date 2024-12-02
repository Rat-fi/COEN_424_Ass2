import time
import pika
from pymongo import MongoClient

client = MongoClient("mongodb://mongodb:27017/")
order_db = client['order_db']
orders_collection = order_db['orders']

def connect_to_rabbitmq():
    for attempt in range(10):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"RabbitMQ not ready yet, retrying ({attempt + 1}/10)...")
            time.sleep(5)
    raise Exception("Failed to connect to RabbitMQ after 10 attempts")

connection = connect_to_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue='user_events')

def callback(ch, method, properties, body):
    event = eval(body.decode())
    account_id = event.get("account_id")
    new_email = event.get("email")
    new_delivery_address = event.get("delivery_address")

    if account_id:
        orders_collection.update_many(
            {"account_id": account_id},
            {"$set": {"email": new_email, "delivery_address": new_delivery_address}}
        )
        print(f"Updated orders for account_id: {account_id}")
    else:
        print("Event missing account_id, ignoring...")

channel.basic_consume(queue='user_events', on_message_callback=callback, auto_ack=True)

print('Listening for events...')
channel.start_consuming()
