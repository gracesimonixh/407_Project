"""
Displays the cumulative equity over time, showing the 
growth of the strategy from the inital capital on a day 
to day basis
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

tf = pd.read_csv("results/TrendFollowing_full_equity.csv", index_col=0)
mr = pd.read_csv("results/MeanReversion_full_equity.csv", index_col=0)
tf.index = pd.to_datetime(tf.index, errors='coerce')
mr.index = pd.to_datetime(mr.index, errors='coerce')

equity_min = min(tf['Portfolio_value'].min(), mr['Portfolio_value'].min()) * 0.95
equity_max = max(tf['Portfolio_value'].max(), mr['Portfolio_value'].max()) * 1.05
dd_min = min(tf['Drawdown'].min(), mr['Drawdown'].min()) * 1.1

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Scatter(x=tf.index, y=tf['Portfolio_value'], 
                        name='Trend Following Equity', 
                        line=dict(color="#5f1c1c", width=3)), 
              secondary_y=False)
fig.add_trace(go.Scatter(x=tf.index, y=tf['Drawdown'], 
                        name='Trend Following DD', 
                        line=dict(color="#a45454", width=1),
                        fill='tozeroy', fillcolor='rgba(164,84,84,0.3)'), 
              secondary_y=True)


fig.update_yaxes(title_text="Equity $", secondary_y=False, range=[equity_min, equity_max], side="left")
fig.update_yaxes(title_text="Drawdown %", secondary_y=True, range=[dd_min, 0], side="right", showgrid=False)
fig.update_xaxes(title_text="Date")
fig.update_layout(
    height=600,  
    title="Equity Curves w/ Drawdown Overlay",
    hovermode='x unified',
    showlegend=True,
    legend=dict(
        orientation="h", 
        yanchor="bottom", 
        y=-0.3,     
        xanchor="center",
        x=0.5,    
        bgcolor="rgba(255,255,255,0.9)"
    )
)

fig.show()

