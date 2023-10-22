import database

client = database.Supa(admin=True)
result = client.list_all_users()
all_users = []
main_dict = {}
# Adani Enterprises,HDFC Bank,Reliance,Tata Motors,ITC,HAL,PayTM,Zomato,CIPLA,BPCL
last_value_for_all_stocks = {
  'Adani Enterprises': 1,
  'HDFC Bank': 1390,
  'Reliance': 1708,
  'Tata Motors': 423,
  'ITC': 152,
  'HAL': 3365,
  'PayTM': 1049,
  'Zomato': 354,
  'CIPLA': 906,
  'BPCL': 661,
  'Tata': 123,
  'Google': 145,
  'Apple': 120,
  'Microsoft': 145.
}

for i in result:
  all_users.append(i.id)
  
for i in all_users:
  value = client.fetch_held_stocks(i)
  for key in value:
    if(key != "total_quantity" and key != "history"):
      return_value = client.operation_insertion(i, key, 'sell', value[key], last_value_for_all_stocks[key], True)
      main_dict[i] = return_value['response']['funds']
print({k: v for k, v in sorted(main_dict.items(), key=lambda item: item[1])})
# print(main_dict)
