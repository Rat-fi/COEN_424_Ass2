# order_microservice.py
from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")
db = client['order_db']
orders_collection = db['orders']

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order = {
        "order_id": data["order_id"],
        "account_id": data["account_id"],
        "items": data["items"],
        "email": data["email"],
        "delivery_address": data["delivery_address"],
        "status": "under process"
    }
    orders_collection.insert_one(order)
    return jsonify({"message": "Order created successfully"}), 201

@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.json
    update_fields = {k: v for k, v in data.items() if k in ["status", "email", "delivery_address"]}
    orders_collection.update_one({"order_id": order_id}, {"$set": update_fields})
    return jsonify({"message": "Order updated successfully"}), 200

@app.route('/orders', methods=['GET'])
def get_orders():
    status = request.args.get("status")
    orders = list(orders_collection.find({"status": status}, {"_id": 0}))
    return jsonify(orders), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
