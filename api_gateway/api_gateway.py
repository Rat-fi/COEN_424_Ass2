from flask import Flask, request, jsonify
import requests
import yaml
import random

app = Flask(__name__)

# Load configuration
with open("gateway_config.yml", "r") as file:
    config = yaml.safe_load(file)

PERCENTAGE = config.get("percentage", 50)

@app.route('/users', methods=['POST'])
def create_user():
    service_url = "http://user_v1:5001" if random.random() < PERCENTAGE / 100 else "http://user_v2:5002"
    response = requests.post(f"{service_url}/users", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/users/<account_id>', methods=['PUT'])
def update_user(account_id):
    service_url = "http://user_v1:5001" if random.random() < PERCENTAGE / 100 else "http://user_v2:5002"
    response = requests.put(f"{service_url}/users/{account_id}", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/orders', methods=['POST', 'PUT', 'GET'])
def route_order_service():
    response = requests.request(request.method, f"http://order_service:5003/orders", json=request.json)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
