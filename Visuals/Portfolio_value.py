import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df1 = pd.read_csv("results/TrendFollowing_full_equity.csv")
df2 = pd.read_csv("results/MeanReversion_full_equity.csv")

df1['Value'] = df1['Portfolio_value']
df2['Value'] = df2['Portfolio_value']

fig = px.line(df1, x='date', y='idk')

fig.show()