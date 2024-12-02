from flask import Flask, request, jsonify
from pymongo import MongoClient
import pika

app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")
db = client['user_db']
users_collection = db['users']

def send_event(event_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='user_events')
    channel.basic_publish(exchange='', routing_key='user_events', body=str(event_data))
    connection.close()

@app.route('/users', methods=['POST'])
def create_user_v2():
    data = request.json
    user = {
        "account_id": data["account_id"],
        "email": data["email"],
        "delivery_address": data["delivery_address"],
        "phone_number": data.get("phone_number", "")
    }
    users_collection.insert_one(user)
    return jsonify({"message": "User created successfully (v2)"}), 201

@app.route('/users/<account_id>', methods=['PUT'])
def update_user(account_id):
    data = request.json
    update_fields = {k: v for k, v in data.items() if k in ["email", "delivery_address"]}

    if update_fields:
        users_collection.update_one({"account_id": account_id}, {"$set": update_fields})

        send_event({"account_id": account_id, **update_fields})

    return jsonify({"message": "User updated successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
