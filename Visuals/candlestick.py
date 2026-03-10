import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('Data/clean_stock_data.csv', parse_dates=['Date'])

aapl = df[df['Ticker']=='AAPL'].sort_values('Date').reset_index(drop=True)
jnj = df[df['Ticker']=='JNJ'].sort_values('Date').reset_index(drop=True)
spy = df[df['Ticker']=='SPY'].sort_values('Date').reset_index(drop=True)

fig = go.Figure()

fig.add_trace(go.Candlestick(x=aapl['Date'], open=aapl['Open'], high=aapl['High'], low=aapl['Low'], close=aapl['Close'], name='AAPL', increasing=dict(line=dict(color='green'), fillcolor='green'), decreasing=dict(line=dict(color='yellow'), fillcolor='yellow')))
fig.add_trace(go.Candlestick(x=jnj['Date'], open=jnj['Open'], high=jnj['High'], low=jnj['Low'], close=jnj['Close'], name='JNJ', increasing=dict(line=dict(color='blue'), fillcolor='blue'), decreasing=dict(line=dict(color='pink'), fillcolor='pink')))
fig.add_trace(go.Candlestick(x=spy['Date'], open=spy['Open'], high=spy['High'], low=spy['Low'], close=spy['Close'], name='SPY', increasing=dict(line=dict(color='purple'), fillcolor='purple'), decreasing=dict(line=dict(color='red'), fillcolor='red')))

fig.update_layout(title="AAPL, JNJ, SPY Candlestick", yaxis_title="Price $", xaxis_title='Date', height=600, showlegend=True)

fig.show()