"""
Displays the cumulative equity over time, showing the 
growth of the strategy from the inital capital on a day 
to day basis
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

mr = pd.read_csv("results/MeanReversion_full_equity.csv", parse_dates=['Date'], index_col='Date')
tf = pd.read_csv("results/TrendFollowing_full_equity.csv", parse_dates=['Date'], index_col='Date')

mr.index.name = "Date"
tf.index.name = "Date"

df = pd.concat([mr["Portfolio_value"], tf["Portfolio_value"]], axis=1).dropna()
df.columns = ["Mean Reversion", "Trend Following"]

df = df / df.iloc[0] * 100

df_long = df.reset_index().melt(id_vars="Date", var_name="Strategy", value_name="Equity")

fig = px.line(df_long, x="Date", y="Equity", color="Strategy", title="Equity Curve Comparison", template="plotly_white")

#fig = make_subplots(rows=2, cols=1, subplot_titles=('Equity Curves', 'Drawdowns'), shared_xaxes=True)
#fig.add_trace(go.Scatter(x=tf.index, y=tf['Portfolio_value'], name='Trend Folowing', line=dict(color='#f67280', width=3)), row=1, col=1)
#fig.add_trace(go.Scatter(x=mr.index, y=mr['Portfolio_value'], name='Mean Reversion', line=dict(color='#5d608d', width=3)), row=1, col=1)

#fig.add_trace(go.Scatter(x=tf.index, y=tf['Drawdown'], name='Trend DD', line=dict(color='#f67280', dash='dash'), fill='tozeroy', fillcolor='rgba(246, 114, 128,0.3)'),row=2, col=1)
#fig.add_trace(go.Scatter(x=mr.index, y=mr['Drawdown'], name='Mean Rev DD', line=dict(color='#f67280', dash='dot'), fill='tozeroy', fillcolor='rgba(93, 96, 141,0.3)'),row=2, col=1)

#fig.update_yaxes(title_text='Portfolio Value $', row=1, col=1)
#fig.update_yaxes(title_text="Drawdown %", row=2, col=1)
#fig.update_xaxes(title_text='Date')

#fig.update_layout(height = 600, title_text="strat comp", title_x=0.5, hovermode='x unified', showlegend=True)

fig.update_layout(hovermode="x unified", yaxis_title="Growth of $100")

fig.show()