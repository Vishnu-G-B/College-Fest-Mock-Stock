from flask_wtf.csrf import Blueprint, request
from flask_cors import CORS
from flask import session
import json
import database
import global_var
import pandas as pd

home_bp = Blueprint("home", __name__, url_prefix="/api/v1/home")

CORS(home_bp)

@home_bp.route("/operation", methods=["POST"])
def buy_stocks():
    if request.method == "POST":
        # short selling check for quantity if quantity is equal to zero
        # buy back (opposite of selling) if quantity is negative
        current_df = pd.read_csv("./current_stock_counter.csv")
        client = database.Supa()
        user_id: str = request.json.get("userId", None)
        stock_name: str = request.json.get("stockName", None)
        operation: str = request.json.get("operation", None)
        quantity: int = int(request.json.get("quantity", None))
        current_value: int = global_var.df[stock_name][current_df.iat[0, 0] - 1]
        return_value = client.operation_insertion(user_id,
            stock_name, operation, quantity, current_value)
        return_value["response"]["held_stocks"] = client.fetch_held_stocks(user_id)
        return json.dumps(return_value["response"])


@home_bp.route("/getstock", methods=["GET"])
def get_stock():
    if request.method == "GET":
        current_values: list = []
        temp_values: dict = {}
        for count, stocks in enumerate(global_var.all_stocks):
            try:
                data = global_var.df[stocks][global_var.current_stock_counter]
            except KeyError:
                return json.dumps({"error": "no more values"})
            temp_values["id"] = count + 1
            temp_values["name"] = stocks
            temp_values["price"] = str(data)
            current_values.append(temp_values)
            temp_values = {}
        global_var.current_stock_counter += 1
        return json.dumps(current_values)


@home_bp.route("/getfunds", methods=["POST"])
def get_funds():
    if request.method == "POST":
        user_id: str = request.json.get("userId", None)
        client = database.Supa()
        data = client.fetch_funds(user_id)
        print(data)
        return data.data


@home_bp.route("/getheldstocks", methods=["POST"])
def get_held_stocks():
    if request.method == "POST":
      user_id: str = request.json.get("userId", None)
      client = database.Supa()
      data = client.fetch_held_stocks(user_id)
      return json.dumps(data)
