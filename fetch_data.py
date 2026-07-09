import yfinance as yf
import pandas as pd
import os

def fetch_data_for_region(market_index, bank_tickers, start_date="1999-01-01", end_date=None):
    if end_date is None:
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
        
    if market_index.startswith("TODO"):
        print(f"Market index {market_index} is marked as TODO. Skipping fetch.")
        return False
        
    bank_tickers = [b for b in bank_tickers if not b.startswith("TODO")]
    tickers = bank_tickers + [market_index]
    
    print(f"Fetching data for {len(tickers)} tickers from {start_date} to {end_date}...")
    
    try:
        data = yf.download(tickers, start=start_date, end=end_date)['Close']
    except Exception as e:
        print(f"Error fetching data: {e}")
        return False
        
    if data.empty:
        print("No data fetched. Please check the tickers.")
        return False
        
    # Ensure columns are sorted nicely (market first, then banks)
    # yfinance sometimes returns a Series if only 1 ticker is fetched, but we always have index + at least 1 bank
    valid_market = [market_index] if market_index in data.columns else []
    valid_banks = [b for b in bank_tickers if b in data.columns]
    
    if not valid_market:
        print(f"Warning: Market index {market_index} not found in fetched data.")
        return False
        
    data = data[valid_market + valid_banks]
    
    # Calculate daily returns (percentage change)
    returns = data.pct_change().dropna(how='all')
    
    if returns.empty:
        print("Fetched data contains no valid return rows. Tickers might be delisted or recently listed.")
        return False
    
    output_file = 'bank_returns.csv'
    returns.to_csv(output_file)
    print(f"Successfully saved daily returns to {output_file}")
    
    print(f"\nTotal Trading Days Fetched: {len(returns)}")
    return True

if __name__ == "__main__":
    # Fallback to US if run directly
    fetch_data_for_region('^GSPC', ['JPM', 'BAC', 'C', 'WFC', 'GS', 'MS'])
