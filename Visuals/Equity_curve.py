"""
Displays the cumulative equity over time, showing the 
growth of the strategy from the inital capital on a day 
to day basis
"""
import pandas as pd
import plotly.express as px

mr = pd.read_csv("MeanReversion_full_equity.csv", parse_dates=[0], index_col=0)
tf = pd.read_csv("TrendFollowing_full_equity.csv", parse_dates=[0], index_col=0)

mr_equity = mr["Portfolio_value"]
tf_equity = tf["Portfolio_value"]

df = pd.concat([mr_equity, tf_equity], axis=1)
df.columns = ["Mean Reversion", "Trend Following"]

df = df / df.iloc[0] * 100

df_long = df.reset_index().melt(id_vars="Date", var_name="Strategy", value_name="Equity")

fig = px.line(df_long, x="Date", y="Equity", color="Strategy", title="Equity Curve Comparison")
fig.show()