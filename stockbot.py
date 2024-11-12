# stockbot.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime
import os
import re
from twilio.twiml.messaging_response import MessagingResponse


# Initialize Flask app
app = Flask(__name__)

# MongoDB configuration (set MongoDB connection string as an environment variable)
MONGO_URI = os.getenv("MONGO_URI", "your_mongodb_connection_string")
client = MongoClient(MONGO_URI)
db = client.stockbot_db
transactions_collection = db.transactions

# Utility functions
def get_current_stock(product_id):
    """Calculate current stock for a given product based on transactions."""
    pipeline = [
        {"$match": {"product_id": product_id}},
        {"$group": {"_id": None, "total_stock": {"$sum": "$count"}}}
    ]
    result = list(transactions_collection.aggregate(pipeline))
    return result[0]["total_stock"] if result else 0

def log_transaction(product_id, action, count):
    """Log a transaction in the MongoDB."""
    transaction = {
        "transaction_id": str(uuid4()),
        "action": action,
        "product_id": product_id,
        "count": count,
        "timestamp": datetime.utcnow().isoformat()
    }
    transactions_collection.insert_one(transaction)

# Bot routes and logic
@app.route("/webhook", methods=["POST"])
def webhook():
   # data = request.get_json()
# Use request.form to parse x-www-form-urlencoded data
    data = request.form
    message_text = data.get("Body", "").lower()
    product_id = data.get("product_id", "default_product")  # Example product handling
    user_message = message_text.strip()

# Create a MessagingResponse object to send a reply
    response = MessagingResponse()

    # Check stock command
    if re.search(r"\b(how many units in stock)\b", user_message):
        current_stock = get_current_stock(product_id)
        response_message = f"We currently have {current_stock} units in stock."
       # return jsonify({"reply": response_message})
        response.message(response_message)
        return str(response)

    # Add stock command
    match = re.match(r"add (\d+)", user_message)
    if match:
        count = int(match.group(1))
        log_transaction(product_id, "Add", count)
        current_stock = get_current_stock(product_id)
        response_message = f"{count} units added. Stock remaining: {current_stock} units."
        #return jsonify({"reply": response_message})
        response.message(response_message)
        return str(response)

    # Reduce stock command
    match = re.match(r"reduce (\d+)", user_message)
    if match:
        count = int(match.group(1))
        current_stock = get_current_stock(product_id)
        if current_stock < count:
            response_message = "Error: Unable to reduce. Insufficient stock."
        else:
            log_transaction(product_id, "Reduce", -count)
            current_stock = get_current_stock(product_id)
            response_message = f"{count} units reduced. Stock remaining: {current_stock} units."
        #return jsonify({"reply": response_message})
        response.message(response_message)
        return str(response)

    # Invalid command
    response_message = "Sorry, I didn't understand the command. Try something like 'Add 10' or 'How many units in stock?'"
    #return jsonify({"reply": response_message})
    response.message(response_message)
    return str(response)

# Error handler
@app.errorhandler(500)
def internal_error(error):
    #return jsonify({"reply": "Internal server error. Please try again later."}), 500
    response.message("Internal server error. Please try again later.")

# Main function for AWS Lambda deployment with Zappa
if __name__ == "__main__":
    app.run(debug=True)

