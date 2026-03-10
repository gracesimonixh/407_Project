import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

df = pd.read_csv('Data/clean_stock_data.csv')

fig = go.Figure(data=[go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])

fig.show()