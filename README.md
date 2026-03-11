# Algorithmic Backtesting Engine

## Overview
Python backtesting engine for simulating trades based on historical stock data. The goal of this backtesting engine is to evaluate and compare different strategies using simulated outcomes.  


## Features
- 

## Strategies

### Trend following
A strategy that attemps to profit from sustained price movements

- **Idea:** Prices that are rising tend to keep rising, and prices that are falling tend to keep falling
- **Buy:** When indicators signal an upward trend 
- **Sell/Short:** When indicators signal a downward trend
- **Exit:** When the trend reverses or a stop-loss is triggered 

### Mean Reversion 
A strategy based on the idea that prices tend to return to their average over time

- **Idea:** If price moves too far from its average, it will eventurally move back
- **Buy:** When price drops significantly below the average
- **Sell/Short:** When price risses significantly above the average 
- **Exit:** When price returns toward the average or a stop loss is triggered


## Installation

```bash
pip install pandas
```

