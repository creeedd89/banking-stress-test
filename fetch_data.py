import yfinance as yf
import pandas as pd
import os

def main():
    # Define the tickers
    banks = ['JPM', 'BAC', 'C', 'WFC', 'GS', 'MS', 'USB', 'PNC', 'COF']

    market = ['^GSPC']
    tickers = banks + market

    # Define the timeframe
    # We need data well before 2019 to have a 255-day estimation window for the first event
    start_date = "2018-01-01"
    end_date = "2026-07-05" # Current date

    print(f"Fetching data for {len(tickers)} tickers from {start_date} to {end_date}...")
    
    # Download data
    data = yf.download(tickers, start=start_date, end=end_date)['Close']
    
    # Ensure columns are sorted nicely (market first, then banks)
    data = data[market + banks]
    
    # Calculate daily returns (percentage change)
    returns = data.pct_change().dropna()
    
    # Save to CSV
    output_file = 'bank_returns.csv'
    returns.to_csv(output_file)
    print(f"Successfully saved daily returns to {output_file}")
    
    # Print a quick preview
    print("\nData Preview:")
    print(returns.head())
    print(f"\nTotal Trading Days: {len(returns)}")

if __name__ == "__main__":
    main()
