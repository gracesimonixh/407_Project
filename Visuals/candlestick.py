import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('Data/clean_stock_data.csv', parse_dates=['Date'])

aapl = df[df['Ticker']=='AAPL'].sort_values('Date').reset_index(drop=True)
jnj = df[df['Ticker']=='JNJ'].sort_values('Date').reset_index(drop=True)
spy = df[df['Ticker']=='SPY'].sort_values('Date').reset_index(drop=True)

fig = go.Figure()

fig.add_trace(go.Candlestick(x=aapl['Date'], open=aapl['Open'], high=aapl['High'], low=aapl['Low'], close=aapl['Close'], name='AAPL', increasing=dict(line=dict(color='#08244f'), fillcolor='#08244f'), decreasing=dict(line=dict(color='#7db2e6'), fillcolor='#7db2e6')))
fig.add_trace(go.Candlestick(x=jnj['Date'], open=jnj['Open'], high=jnj['High'], low=jnj['Low'], close=jnj['Close'], name='JNJ', increasing=dict(line=dict(color='#5f1c1c'), fillcolor='#5f1c1c'), decreasing=dict(line=dict(color='#a45454'), fillcolor='#a45454')))
fig.add_trace(go.Candlestick(x=spy['Date'], open=spy['Open'], high=spy['High'], low=spy['Low'], close=spy['Close'], name='SPY', increasing=dict(line=dict(color="#2a095b"), fillcolor='#2a095b'), decreasing=dict(line=dict(color="#ac8fd8"), fillcolor='#ac8fd8')))

fig.update_layout(title="AAPL, JNJ, SPY Candlestick", yaxis_title="Price $", xaxis_title='Date', height=600, showlegend=True, template='plotly_dark')

fig.show()