import database
import pandas as pd

client = database.Supa(admin=True)
result = client.list_all_users()
all_users = []
main_dict = {}
df = pd.read_csv("./PRICE_LIST.csv")
af = pd.read_csv("./current_stock_counter.csv")
final_price = df.iloc[af["current_stock_counter"][0]]

for indi_user in result:
    remaining_stocks = client.fetch_held_stocks(str(indi_user.id))
    for indi_stock_name in final_price.keys():
        if indi_stock_name in remaining_stocks:
            client.sell_operation(
                indi_user.id,
                indi_stock_name,
                final_price[indi_stock_name],
                remaining_stocks[indi_stock_name],
            )
            print(
                f"sold {indi_user.id} {indi_stock_name} {final_price[indi_stock_name]} {remaining_stocks[indi_stock_name]}"
            )
        if indi_stock_name in remaining_stocks["short_quantity"]:
            client.short_sell_operation(
                indi_user.id,
                indi_stock_name,
                final_price[indi_stock_name],
                remaining_stocks["short_quantity"][indi_stock_name],
            )
            print(
                f"short sold {indi_user.id} {indi_stock_name} {final_price[indi_stock_name]} {remaining_stocks[indi_stock_name]}"
            )
