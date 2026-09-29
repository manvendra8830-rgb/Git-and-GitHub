import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not configured in the .env file.")

client = MongoClient(MONGO_URI)

db = client["git_github_db"]
todo_collection = db["todo_items"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/todo")
def todo():
    return render_template("todo.html")


@app.route("/api")
def api():
    try:
        with open("backend/data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as error:
        return jsonify({"error": str(error)}), 500


@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    try:
        item_name = request.form.get("itemName", "").strip()
        item_description = request.form.get("itemDescription", "").strip()

        if not item_name or not item_description:
            return jsonify({
                "error": "Item Name and Item Description are required."
            }), 400

        todo_item = {
            "itemName": item_name,
            "itemDescription": item_description
        }

        result = todo_collection.insert_one(todo_item)

        return jsonify({
            "message": "To-Do item submitted successfully.",
            "itemId": str(result.inserted_id)
        }), 201

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
