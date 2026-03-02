import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class TradeReturn:
    """
    Bar chart - frequency of winning vs losing trades
    """

    

class WinLoss:
    """
    Pie chart - percentage of winning vs losing trades (win rate)
    """
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Trade Outcomes: Trend Following", "Trade Outcome: Mean Reversion"), specs=[[{"type": "pie"}, {"type": "pie"}]])
    
    df1 = pd.read_csv("results/TrendFollowing_full_trades.csv")
    df1['Result'] = df1['pnl'].apply(lambda x: 'Win' if x > 0 else 'Loss')
    df2 = pd.read_csv("results/MeanReversion_full_trades.csv")
    df2['Result'] = df2['pnl'].apply(lambda x: 'Win' if x > 0 else 'Loss')
    

    labels = df1['Result'].value_counts().index
    values = df1['Result'].value_counts().values

    labels2 = df2['Result'].value_counts().index
    values2 = df2['Result'].value_counts().values

    fig.add_trace(go.Pie(labels=labels, values=values, name="Trend Following", marker=dict(colors=["#f67280", "#5d608d"])), row=1, col=1)
    fig.add_trace(go.Pie(labels=labels2, values=values2, name="Mean Reversion", marker=dict(colors=["#f67280", "#5d608d"])), row=1, col=2)

    fig.update_layout(height=500, showlegend=False)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.show()


  