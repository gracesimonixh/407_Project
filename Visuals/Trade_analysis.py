import plotly.express as px
import pandas as pd

class TradeReturn:
    """
    Bar chart - frequency of winning vs losing trades
    """

    

class WinLoss:
    """
    Pie chart - percentage of winning vs losing trades (win rate)
    """
    df = pd.read_csv("results/TrendFollowing_full_trades.csv")
    df['Result'] = df['pnl'].apply(lambda x: 'Win' if x > 0 else 'Loss')

    fig = px.pie(df, names='Result', title='Trade outcomes by ticker', color_discrete_sequence=["#9A74B1", "#355C7D"])

    fig.show()

