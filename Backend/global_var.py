from database import Supa
import pandas as pd

all_stocks: list[str] = []

df = pd.read_csv("./PRICE_LIST.csv")
for cols in df.columns:
    all_stocks.append(cols)
max_length = len(df.index)
