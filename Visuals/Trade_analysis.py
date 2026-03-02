import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def tradeAnalysis():
    fig = make_subplots(rows=2, cols=2, subplot_titles=("Trend Following", "Mean Reversion"), 
                        specs=[[{"type": "pie"}, {"type": "pie"}],
                                [{"type": "bar"}, {"type": "bar"}]], vertical_spacing=0.05)
    
    df1 = pd.read_csv("results/TrendFollowing_full_trades.csv")
    df1['Result'] = df1['pnl'].apply(lambda x: 'Win' if x > 0 else 'Loss')
    df2 = pd.read_csv("results/MeanReversion_full_trades.csv")
    df2['Result'] = df2['pnl'].apply(lambda x: 'Win' if x > 0 else 'Loss')

    labels1 = df1['Result'].value_counts().index
    values1 = df1['Result'].value_counts().values

    labels2 = df2['Result'].value_counts().index
    values2 = df2['Result'].value_counts().values

    win_return1 = df1[df1['Result']=='Win']['pnl'].sum()
    loss_return1 = abs(df1[df1['Result']=='Loss']['pnl'].sum())

    win_return2 = df2[df2['Result']=='Win']['pnl'].sum()
    loss_return2 = abs(df2[df2['Result']=='Loss']['pnl'].sum())


    fig.add_trace(go.Pie(labels=labels1, values=values1, name="Trend Following", marker=dict(colors=["#d65f4d", "#670020"])), row=1, col=1)
    fig.add_trace(go.Pie(labels=labels2, values=values2, name="Mean Reversion", marker=dict(colors=["#d65f4d", "#670020"])), row=1, col=2)
    
    fig.add_trace(go.Bar(x=['Wins', 'Losses'], y=[win_return1, loss_return1], name="Trend Following", marker=dict(color=["#d65f4d", "#670020"]), text=[f"${win_return1:.0f}", f"${loss_return1:.0f}"], textposition="inside"), row=2, col=1)
    fig.add_trace(go.Bar(x=['Wins', 'Losses'], y=[win_return2, loss_return2], name="Mean Reversion", marker=dict(color=["#d65f4d", "#670020"]), text=[f"${win_return2:.0f}", f"${loss_return2:.0f}"], textposition="inside"), row=2, col=2)

    fig.update_layout(height=650, showlegend=False, title={'text':"Trade Analysis", 'x':0.5, 'xanchor': 'center', 'y': 0.95}, margin=dict(t=100, b=40, l=40, r=40))
    fig.update_traces(textposition='inside', textinfo='percent+label', selector=dict(type='pie'))
    fig.show()

tradeAnalysis()