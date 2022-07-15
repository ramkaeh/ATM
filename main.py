import json
from datetime import datetime
from time import sleep
import numpy
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from binance.client import Client
from binance.enums import *

# Time data
now = datetime.now()
dt_string = now.strftime("%D-%m-%Y | %H:%M:%S")
print("data startu:", dt_string)
# Accessing account
# From file
"""""
with open('account.json', 'r') as read_file:
    account = json.load(read_file)
    client = Client(
    
        api_key=account["api_key"],
        secret_key = account["secret_key"]
    )
"""
# test version
print("1")
api_key = 'wHU2ToDetca156j2eaNqpPsdHGmgqAiB6Oy7ZHEKnK0sYTFjj2LZIntYwEjXmw45'
secret_key = 'LiQOQjUX1Hyo5e8u3bgzJm1mWtWK9KY93F3IPvY4G1JsSlrHxB11N73Jq0hutEXw'

client = Client(api_key, secret_key)
client.API_URL = 'https://testnet.binance.vision/api'

print("2")

info = client.get_account()
print(info)

# test data
engine = create_engine('sqlite:///CryptoDB.db')
df = pd.read_sql('BTCUSDT', engine)
pd.set_option('display.max_columns', None)
df1 = df.iloc[:, 2]
df['open_price'] = df['open_price'].astype(float)

# test ta
def dema(frame, span):

    ema1 = frame.ewm(span=span, min_periods=1, adjust=True, ignore_na=False, axis=0).mean()
    ema2 = ema1.ewm(span=span, min_periods=1, adjust=True, ignore_na=False, axis=0).mean()
    return 2 * ema1 - ema2

price_dema_short = dema(df1, 10)
price_dema_long = dema(df1, 20)
print("3")

balance = client.get_asset_balance(asset='symbol')

trades = client.get_my_trades(symbol='BTCUSDT')


print(balance)

print(trades)
print('1')
orders = client.get_all_orders(symbol='BTCUSDT', limit=10)

for order in orders:

    pd.options.display.width = 0
    df = pd.DataFrame([order])
    df = df.iloc[:, [0, 1, 5, 7, 8, 11, 14]]
    df['price'] = df['cummulativeQuoteQty'].astype(float) / df['origQty'].astype(float)
    df.columns = ['Symbol', 'OrderID', 'Quantity', 'Paid', 'Status', 'Side', 'Time', 'Price']
    df.Time = pd.to_datetime(df.Time, unit='ms')
    print(df)
"""
order = client.order_market_buy(
    symbol='BTCUSDT',
    quantity=0.001)
print(order)



plt.plot(price_dema_long,color = 'red')
plt.plot(price_dema_short, color='blue')
df["open_price"].plot(color='black')
plt.show()
"""

# Starting trading loop
START = True
""""
while START:
    try:
        #trading loop info
        sleep(3)
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y | %H:%M:%S")
        print("Start pętli, data:", dt_string)
        
    
    except Exception as trader_exception:
        print(trader_exception)
"""""
