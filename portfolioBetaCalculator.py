import pandas as pd
import numpy as np
import yfinance as yf

def get_tickers():
    tickers = input("Enter tickers (format: 'AAPL AMZN BA GOOG IBM MGM T TSLA'): ")
    return tickers

def get_weights():
    weight_input = input("Enter portfolio weights (one for each ticker, same format. \n The format: 0.10 0.20 0.10 0.10 0.20 0.10 0.10 0.10): ")
    equity_weights = weight_input.split()

    for i in range(len(equity_weights)):
        equity_weights[i] = float(equity_weights[i])
    return equity_weights

def download_data(tickers):
    equity_data = yf.download(tickers, start="2012-01-12", end="2020-08-11",)
    market_data = yf.download("^GSPC", start="2012-01-12", end="2020-08-11",)
    return equity_data, market_data

def get_returns(equity_data, market_data):
    equity_close = equity_data["Adj Close"]
    market_close = market_data["Adj Close"]

    equity_returns = equity_close.pct_change()
    market_returns = market_close.pct_change()

    equity_returns.dropna(inplace=True)
    market_returns.dropna(inplace=True)
    market_returns = pd.DataFrame(market_returns)
    market_returns = market_returns.rename(columns={"Adj Close": "SPX"})

    total_returns = pd.concat([equity_returns, market_returns], axis=1)

    return equity_returns, market_close, total_returns

def get_beta(total_returns, equity_weights):
    beta = {}
    alpha = {}

    for i in total_returns.columns:
        if i != 'Date' and i != "SPX":
            b, a = np.polyfit(total_returns['SPX'], total_returns[i], 1)
            beta[i] = b
            alpha[i] = a
            
    t = 0
    p_beta = 0
    for key, value in beta.items(): 
        p_beta += value * equity_weights[t]
        t += 1
    return p_beta

def main():
    tickers = get_tickers()
    equity_weights = get_weights()

    equity_data, market_data = download_data(tickers)

    equity_returns, market_returns, total_returns = get_returns(equity_data, market_data)

    portfolio_beta = get_beta(total_returns, equity_weights)

    print(portfolio_beta)

main()