from binance.client import Client
import pandas as pd
from sqlalchemy import create_engine
import unicorn_binance_websocket_api
import sqlite3


api_key = 'wHU2ToDetca156j2eaNqpPsdHGmgqAiB6Oy7ZHEKnK0sYTFjj2LZIntYwEjXmw45'
secret_key = 'LiQOQjUX1Hyo5e8u3bgzJm1mWtWK9KY93F3IPvY4G1JsSlrHxB11N73Jq0hutEXw'

client = Client(api_key, secret_key)
client.API_URL = 'https://testnet.binance.vision/api'

engine = create_engine('sqlite:///CryptoDB.db')


CUSTOM = 0

tickers = []
prices = client.get_all_tickers()

for coin in prices:
    tickers.append(coin['symbol'])


if CUSTOM:
    symbols = ['BTC', 'ETH', 'BNB', 'LTC']
    symbols = [symbol + 'USDT' for symbol in symbols]
else:
    symbols = tickers


conn = sqlite3.connect('CryptoDB.db')
cursor = conn.cursor()

for ticker in tickers:
    cursor.execute('DROP TABLE IF EXISTS ' + ticker)
    conn.commit()
conn.close()


for symbol in symbols:
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "10 minutes ago UTC")

    for candle in klines:
        df = pd.DataFrame([candle])
        df = df.iloc[:, [0, 6, 1, 2, 3, 4, 5]]
        df.columns = ['kline_start_time', 'kline_close_time', 'open_price', 'close_price', 'high_price', 'low_price', 'base_volume']
        df.close_price = df.close_price.astype(float)
        df.kline_start_time = pd.to_datetime(df.kline_start_time, unit='ms')
        df.kline_close_time = pd.to_datetime(df.kline_close_time, unit='ms')
        df['is_closed'] = 1
        df['symbol'] = symbol
        df.to_sql(symbol, engine, if_exists='append', index=False)


ubwa = unicorn_binance_websocket_api.BinanceWebSocketApiManager(exchange="binance.com")
ubwa.create_stream(['kline_1m'], symbols, output='UnicornFy')


def SQLimport(data):
    klines = data['kline']
    frame = pd.DataFrame([klines])
    frame = frame.loc[:, ['symbol', 'kline_start_time', 'kline_close_time', 'open_price', 'close_price', 'high_price', 'low_price', 'base_volume', 'is_closed']]
    frame.close_price = frame.close_price.astype(float)
    frame.kline_start_time = pd.to_datetime(frame.kline_start_time, unit='ms')
    frame.kline_close_time = pd.to_datetime(frame.kline_close_time, unit='ms')

    if data['kline']['is_closed']:
        frame.to_sql(frame.symbol[0], engine, index=False, if_exists='append')


while True:
    data = ubwa.pop_stream_data_from_stream_buffer()
    if data:
        if len(data) > 3:
            SQLimport(data)