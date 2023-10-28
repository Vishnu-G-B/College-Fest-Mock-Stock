import configparser

from postgrest import exceptions
from supabase import Client, create_client


class Supa:
    def __init__(self, admin=False) -> None:
        config = configparser.ConfigParser()
        config.read("./config.cfg")
        self.supabase_config = config["supabase"]
        if admin == True:
            self.supabase_client = create_client(
                self.supabase_config["base_url"], self.supabase_config["service_role"]
            )

        else:
            self.supabase_client: Client = create_client(
                self.supabase_config["base_url"], self.supabase_config["anon_key"]
            )

    def list_all_users(self):
        result = self.supabase_client.auth.admin.list_users()
        return result

    def sign_user_out(self):
        result = self.supabase_client.auth.sign_out()
        return result

    def sign_user_up(self, email: str, password: str):
        result = self.supabase_client.auth.sign_up(
            {"email": f"{email}", "password": f"{password}"}
        )
        return result

    def sign_user_in(self, email: str, password: str):
        result = self.supabase_client.auth.sign_in_with_password(
            {"email": f"{email}", "password": f"{password}"}
        )
        return result

    def create_users_funds(self, user_id: str):
        try:
            data = (
                self.supabase_client.table("funds_table")
                .insert(
                    {
                        "user_id": f"{user_id}",
                    }
                )
                .execute()
            )
        except exceptions.APIError:
            data = {"funds": "already exists"}

        return data

    def fetch_funds(self, user_id: str):
        data = (
            self.supabase_client.table("funds_table")
            .select("funds")
            .eq("user_id", f"{user_id}")
            .execute()
        )
        return data

    def set_funds(self, user_id: str, new_funds: float):
        data = (
            self.supabase_client.table("funds_table")
            .update(
                {
                    "funds": f"{new_funds}",
                }
            )
            .eq("user_id", user_id)
            .execute()
        )
        return data

    def short_sell_operation(
        self, user_id: str, stock_name: str, current_stock_value: int, quantity: int
    ):
        required_operations: list[dict] = (
            self.supabase_client.table("main_ops_table")
            .select("id", "stock_name", "quantity", "operation", "current_stock_value")
            .eq("user_id", user_id)
            .eq("operation", "short_buy")
            .eq("in_hand", True)
            .limit(quantity)
            .execute()
            .data
        )
        short_buy_quantity = 0
        for obj in required_operations:
            short_buy_quantity += obj["quantity"]
        print(short_buy_quantity)
        if short_buy_quantity >= quantity:
            current_funds: int = self.fetch_funds(user_id).data[0]["funds"]
            for indi_dict in required_operations:
                for i in range(0, quantity):
                    profit_or_loss: int = (
                        indi_dict["current_stock_value"] - current_stock_value
                    )
                    print(profit_or_loss)
                    current_funds += profit_or_loss + indi_dict["current_stock_value"]
                if indi_dict["quantity"] - quantity == 0:
                    self.supabase_client.table("main_ops_table").update(
                        {"in_hand": False, "quantity": indi_dict["quantity"] - quantity}
                    ).eq("id", indi_dict["id"]).eq("operation", "short_buy").execute()
                else:
                    self.supabase_client.table("main_ops_table").update(
                        {"quantity": indi_dict["quantity"] - quantity}
                    ).eq("id", indi_dict["id"]).eq("operation", "short_buy").execute()
            data = (
                self.supabase_client.table("main_ops_table")
                .insert(
                    {
                        "user_id": f"{user_id}",
                        "stock_name": f"{stock_name}",
                        "operation": "short_sell",
                        "quantity": f"{quantity}",
                        "current_stock_value": f"{current_stock_value}",
                        "in_hand": True,
                        # "quantity_before_buying": f"{quantity_before_buying}",
                    }
                )
                .execute()
            )
            print(current_funds)
            new_funds: int = self.set_funds(user_id, current_funds).data[0]["funds"]
            held_stocks: list[dict] = self.fetch_held_stocks(user_id)
            return {"response": {"funds": int(new_funds), "held_stocks": held_stocks}}
        else:
            return {"response": {"error": "INSUFFICIENT BUY QUANTITY"}}

    def sell_operation(
        self, user_id: str, stock_name: str, current_stock_value: int, quantity: int
    ):
        held_stocks: list[dict] = self.fetch_held_stocks(user_id)
        short_buy_stocks: list[dict] = (
            self.supabase_client.table("main_ops_table")
            .select("id", "stock_name", "quantity", "operation", "current_stock_value")
            .eq("stock_name", stock_name)
            .eq("user_id", user_id)
            .eq("operation", "short_buy")
            .eq("in_hand", True)
            .limit(quantity)
            .execute()
            .data
        )
        short_buy_quantity = 0
        for obj in short_buy_stocks:
            short_buy_quantity += obj["quantity"]
        try:
            if held_stocks[stock_name] - short_buy_quantity >= quantity:
                funds_before_sell: int = self.fetch_funds(user_id).data[0]["funds"]
                funds_after_sell: int = funds_before_sell + (
                    current_stock_value * quantity
                )
                self.set_funds(user_id, funds_after_sell)

                self.supabase_client.table("main_ops_table").insert(
                    {
                        "user_id": f"{user_id}",
                        "stock_name": f"{stock_name}",
                        "operation": "sell",
                        "quantity": f"{quantity}",
                        "current_stock_value": f"{current_stock_value}",
                    }
                ).execute()

                held_stocks: list[dict] = self.fetch_held_stocks(user_id)
                return {
                    "response": {
                        "funds": int(funds_after_sell),
                        "held_stocks": held_stocks,
                    }
                }
            else:
                return {
                    "response": {
                        "error": f"INSUFFICIENT STOCK QUANTITY FOR {stock_name}"
                    }
                }
        except KeyError:
            return {"response": {"error": f"NO HELD STOCKS FOR {stock_name}"}}

    def buy_operation(
        self,
        user_id: str,
        stock_name: str,
        current_stock_value: int,
        quantity: int,
        short_buy: bool = False,
    ):
        user_current_funds: int = self.fetch_funds(user_id).data[0]["funds"]
        stock_value: int = current_stock_value * quantity
        if stock_value > user_current_funds:
            # print("insufficient Funds")
            return {"response": {"error": "INSUFFICIENT FUNDS"}}
        else:
            funds_after_buy: int = user_current_funds - stock_value
            new_funds: int = self.set_funds(user_id, funds_after_buy).data[0]["funds"]
            data = (
                self.supabase_client.table("main_ops_table")
                .insert(
                    {
                        "user_id": f"{user_id}",
                        "stock_name": f"{stock_name}",
                        "operation": "short_buy" if short_buy else "buy",
                        "quantity": f"{quantity}",
                        "current_stock_value": f"{current_stock_value}",
                        "in_hand": True,
                        # "quantity_before_buying": f"{quantity_before_buying}",
                    }
                )
                .execute()
            )
            final_held_stocks: dict = self.fetch_held_stocks(user_id)
            return {
                "response": {"funds": new_funds, "held_stocks": final_held_stocks},
            }

    def operation_insertion(
        self,
        user_id: str,
        stock_name: str,
        operation: str,
        quantity: int,
        bought_at: float,
        admin_overide=False,
    ):
        return_value = {}
        held_stocks = self.fetch_held_stocks(user_id)
        data = self.fetch_funds(user_id)
        insert = True
        if operation == "buy":
            value = quantity * bought_at
            current_funds = data.data[0]["funds"]
            try:
                if held_stocks[stock_name] < 0:
                    print("SHORT BUY")
                    normal_buy = held_stocks[stock_name] + quantity
                    short_buy = abs(held_stocks[stock_name])
                    current_funds -= normal_buy * bought_at
                    print("FUNDS AFTER NORMAL BUY", current_funds)
                    current_funds -= short_buy * bought_at
                    print("FUNDS AFTER SHORT BUY", current_funds)
                    if not admin_overide:
                        response = self.set_funds(user_id, current_funds)
                        return_value["funds"] = response.data[0]["funds"]
                        insert = True
                    else:
                        return_value["funds"] = current_funds
                elif current_funds >= value:
                    print("COMPLETE NORMAL BUY")
                    current_funds -= value
                    print("FUNDS AFTER COMPLETE NORMAL BUY", current_funds)
                    if not admin_overide:
                        response = self.set_funds(user_id, current_funds)
                        # print(response.data[0]['funds'])
                        return_value["funds"] = response.data[0]["funds"]
                        insert = True
                    else:
                        return_value["funds"] = current_funds

                elif current_funds < value:
                    return_value = {"error": "INSUFFICIENT FUNDS"}
                    insert = False

            except KeyError:
                if current_funds >= value:
                    print("COMPLETE NORMAL BUY")
                    current_funds -= value
                    print("FUNDS AFTER COMPLETE NORMAL BUY", current_funds)
                    if not admin_overide:
                        response = self.set_funds(user_id, current_funds)
                        # print(response.data[0]['funds'])
                        return_value["funds"] = response.data[0]["funds"]
                        insert = True
                    else:
                        return_value["funds"] = current_funds
                elif current_funds < value:
                    return_value = {"error": "INSUFFICIENT FUNDS"}
                    insert = False

        if operation == "sell":
            insert = True
            try:
                if quantity > held_stocks[stock_name]:
                    print("SHORT SELL")
                    short_sell = quantity - held_stocks[stock_name]
                    short_value = short_sell * bought_at
                    if short_value <= data.data[0]["funds"]:
                        normal_sell = held_stocks[stock_name]
                        value = normal_sell * bought_at
                        current_funds = data.data[0]["funds"]
                        current_funds += value
                        print("FUNDS AFTER NORMAL SELL", current_funds)
                        current_funds += short_value
                        if current_funds < 2000000:
                            print("FUNDS AFTER SHORT_SELL", current_funds)
                            if not admin_overide:
                                response = self.set_funds(user_id, current_funds)
                                return_value["funds"] = response.data[0]["funds"]
                                insert = True
                            # return_value = {'error': 'Selling more than you own'}
                            # insert = False
                            else:
                                return_value["funds"] = current_funds
                        else:
                            return_value["funds"] = current_funds

                    else:
                        return_value = {"error": "INSUFFICIENT FUNDS"}
                        insert = False
                else:
                    print("NORMAL SELL")
                    value = quantity * bought_at
                    current_funds = data.data[0]["funds"]
                    current_funds += value
                    print("FUNDS AFTER NORMAL SELL", current_funds)
                    if not admin_overide:
                        response = self.set_funds(user_id, current_funds)
                        return_value["funds"] = response.data[0]["funds"]
                        insert = True
                    else:
                        return_value["funds"] = current_funds

            except KeyError:
                # return_value = {'error': "You don't own any of this companies stock"}
                print("SHORT SELL WHEN YOU HAVE 0 QUANTITY")
                short_sell = quantity
                short_value = short_sell * bought_at
                if short_value <= data.data[0]["funds"]:
                    current_funds = data.data[0]["funds"]
                    current_funds -= short_value
                    print("FUNDS AFTER SHORT SELL", current_funds)
                    if not admin_overide:
                        response = self.set_funds(user_id, current_funds)
                        return_value["funds"] = response.data[0]["funds"]
                        insert = True
                    else:
                        return_value["funds"] = current_funds
                else:
                    return_value = {"error": "INSUFFICIENT FUNDS"}
                    insert = False
        if insert == True and not admin_overide:
            try:
                quantity_before_buying = held_stocks[stock_name]
            except KeyError:
                quantity_before_buying = 0
            data = (
                self.supabase_client.table("main_ops_table")
                .insert(
                    {
                        "user_id": f"{user_id}",
                        "stock_name": f"{stock_name}",
                        "operation": f"{operation}",
                        "quantity": f"{quantity}",
                        "bought_at": f"{bought_at}",
                        "quantity_before_buying": f"{quantity_before_buying}",
                    }
                )
                .execute()
            )
        else:
            data = "empty"

        return {"data": data, "response": return_value}

    def fetch_held_stocks(self, user_id: str):
        held_stocks_w_history = {"short_quantity": {}}
        all_operations: list[dict] = (
            (
                self.supabase_client.table("main_ops_table")
                .select("stock_name", "quantity", "current_stock_value", "operation")
                .eq("user_id", user_id)
            )
            .execute()
            .data
        )
        for indiDict in all_operations:
            if indiDict["stock_name"] not in held_stocks_w_history:
                held_stocks_w_history[indiDict["stock_name"]] = 0
                held_stocks_w_history["short_quantity"][indiDict["stock_name"]] = 0
            if indiDict["operation"] == "buy":
                held_stocks_w_history[indiDict["stock_name"]] += indiDict["quantity"]
            elif indiDict["operation"] == "sell":
                held_stocks_w_history[indiDict["stock_name"]] -= indiDict["quantity"]
            elif indiDict["operation"] == "short_buy":
                held_stocks_w_history["short_quantity"][
                    indiDict["stock_name"]
                ] += indiDict["quantity"]
        held_stocks_w_history["history"] = all_operations
        return held_stocks_w_history
