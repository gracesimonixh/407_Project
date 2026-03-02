"""
Displays the cumulative equity over time, showing the 
growth of the strategy from the inital capital on a day 
to day basis
"""
import pandas as pd
import plotly.express as px

mr = pd.read_csv("results\MeanReversion_full_equity.csv", parse_dates=[0], index_col=0)
tf = pd.read_csv("results\TrendFollowing_full_equity.csv", parse_dates=[0], index_col=0)

mr.index.name = "Date"
tf.index.name = "Date"

df = pd.concat([mr["Portfolio_value"], tf["Portfolio_value"]], axis=1).dropna()
df.columns = ["Mean Reversion", "Trend Following"]

df = df / df.iloc[0] * 100

df_long = df.reset_index().melt(id_vars="Date", var_name="Strategy", value_name="Equity")

fig = px.line(df_long, x="Date", y="Equity", color="Strategy", title="Equity Curve Comparison", template="plotly_white")

fig.update_layout(hovermode="x unified", yaxis_title="Growth of $100")

fig.show()