from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from binance.client import Client



api_key = 'wHU2ToDetca156j2eaNqpPsdHGmgqAiB6Oy7ZHEKnK0sYTFjj2LZIntYwEjXmw45'
secret_key = 'LiQOQjUX1Hyo5e8u3bgzJm1mWtWK9KY93F3IPvY4G1JsSlrHxB11N73Jq0hutEXw'

client = Client(api_key, secret_key)
client.API_URL = 'https://testnet.binance.vision/api'

engine = create_engine('sqlite:///CryptoDB.db')

symbols = ['BTC', 'ETH', 'BNB', 'LTC', 'TRX', 'XRP']
df = pd.read_sql('BTCUSDT', engine)
pd.set_option('display.max_columns', None)

def dema(frame, span):

    ema1 = frame.ewm(span=span, min_periods=1, adjust=True, ignore_na=False, axis=0).mean()
    ema2 = ema1.ewm(span=span, min_periods=1, adjust=True, ignore_na=False, axis=0).mean()
    return 2 * ema1 - ema2

def rsi(frame,span):

    #frame = frame.to_frame()
    frame['diff'] = frame.diff(1)
    frame['gain'] = frame['diff'].clip(lower=0).round(2)
    frame['loss'] = frame['diff'].clip(upper=0).abs().round(2)
    frame['avg_gain'] = frame['gain'].rolling(window=span, min_periods=span).mean()[:span + 1]
    frame['avg_loss'] = frame['loss'].rolling(window=span, min_periods=span).mean()[:span + 1]

    for i, row in enumerate(frame['avg_gain'].iloc[span+1:]):
        frame['avg_gain'].iloc[i + span + 1] = \
            (frame['avg_gain'].iloc[i + span] * (span - 1) + frame['gain'].iloc[i + span + 1]) / span

    for i, row in enumerate(frame['avg_loss'].iloc[span+1:]):
        frame['avg_loss'].iloc[i + span + 1] = \
            (frame['avg_loss'].iloc[i + span] * (span - 1) + frame['loss'].iloc[i + span + 1]) / span

    frame['rs'] = frame['avg_gain'] / frame['avg_loss']
    frame['rsi'] = 100 - (100/(1.0 + frame['rs']))

    return frame

def volatility(frame):

    #frame = frame.to_frame()
    frame['Log returns'] = np.log(frame['close_price'] / frame['close_price'].shift())

    return frame


df = df.iloc[:,3]
df = df.to_frame()
rsi = rsi(df,14)
vol = volatility(df)
print(vol)
#print(rsi)
#rsi.to_csv('dane.csv')
'''
plt.grid()
plt.plot(dema1,color='red')
plt.plot(dema2,color='black')
plt.plot(rsi['rsi'], color='red')
plt.plot(rsi1['rsi'], color='blue')
plt.plot(rsi2['rsi'], color='black')
plt.plot(df)
plt.show()
'''