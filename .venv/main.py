import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#Import necessary libraries

ticker = input("Enter the stock symbol you wish to track: (ex. AAPL): ").upper()
#Lets the user type in a stock symbol


end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
#Gets the current date and sets the start date to the year prior

data = yf.download(ticker, start = start_date, end = end_date, interval = "1h")
#Downloads hourly prices from Yahoo Finance

data['SMA_10'] = data['Close'].rolling(window = 10).mean()
data['SMA_50'] = data['Close'].rolling(window = 50).mean()
#SMA = Simple Moving Average: The program takes the average of the last 20 and last 100 closing prices

data['Signal'] = (data['SMA_10'] > data['SMA_50']).astype(int)

data['Position'] = data['Signal'].diff()
#If 20 day is greater than 100 day, buy indicator, otherwise sell indicator

plt.style.use('seaborn-v0_8-darkgrid')

plt.figure(figsize=(16,8))
plt.plot(data['Close'], label = 'Closing Price', alpha = 0.5)
plt.plot(data['SMA_10'], label = '10-Day SMA', color = 'green', linewidth = 2)
plt.plot(data['SMA_50'], label = '50-Day SMA', color = 'red', linewidth = 2)
#Sets graph style and plots price, SMA 10 day, and SMA 50 day graphs

plt.plot(data.loc[data['Position'] == 1].index,
         data.loc[data['Position'] == 1, 'SMA_10'],
         '^', markersize=12, color='green', label='Buy Signal')

plt.plot(data.loc[data['Position'] == -1].index,
         data.loc[data['Position'] == -1, 'SMA_10'],
         'v', markersize=12, color='red', label='Sell Signal')
#Places green arrows at buy locations and red arrows at sell locations

plt.title(f"{ticker} - SMA Crossover Strategy ({start_date} to {end_date})", fontsize = 16)
plt.xlabel('Date')
plt.ylabel('Price ($)')
plt.xticks(rotation = 45)
plt.legend()
plt.tight_layout()
plt.grid(True)
plt.show()
#Final plot labeling and presentation

# Backtesting
starting_cash = 10000  # pretend you start with $10,000
cash = starting_cash
shares = 0  # how many shares you currently own

for date, row in data.iterrows():
    if row['Position'].item() == 1:  # Buy signal
        if cash > 0:
            shares = cash / row['Close'].item()  # buy as many shares as you can
            cash = 0
            print(f"BUY  on {date.date()} at ${row['Close'].item():.2f}")

    elif row['Position'].item() == -1:  # Sell signal

        if shares > 0:
            cash = shares * row['Close'].item()  # sell everything
            shares = 0
            print(f"SELL on {date.date()} at ${row['Close'].item():.2f}")

# At the end, calculate what everything is worth
final_value = cash + (shares * data['Close'].iloc[-1].item())
buy_and_hold = (data['Close'].iloc[-1].item() / data['Close'].iloc[0].item() - 1) * 100
profit = final_value - starting_cash
percent_return = (profit / starting_cash) * 100

print(f"\n--- Results ---")
print(f"Starting money:  ${starting_cash:,.2f}")
print(f"Ending value:    ${final_value:,.2f}")
print(f"Profit/Loss:     ${profit:,.2f}")
print(f"Return:          {percent_return:.2f}%")
print(f"Buy & Hold Return: {buy_and_hold:.2f}%")
print(f"Strategy vs Buy & Hold: {percent_return - buy_and_hold:.2f}%")
