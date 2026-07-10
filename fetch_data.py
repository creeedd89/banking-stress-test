import pandas as pd
import os
import streamlit as st
from data_sources.yfinance_source import YFinanceSource
from data_sources.stooq_source import StooqSource
from data_sources.local_csv_source import LocalCSVSource
from data_sources.fallback import FallbackChain, DataUnavailableError

def setup_fallback_chain() -> FallbackChain:
    """Configures the order of data sources to try."""
    return FallbackChain([
        YFinanceSource(),
        StooqSource(),
        LocalCSVSource()
    ])

@st.cache_data(show_spinner=False)
def fetch_data_for_region(country: str, market_index: str, bank_tickers: list, start_date="1999-01-01", end_date=None, min_rows: int = 100, event_date: str = None) -> pd.DataFrame:
    if end_date is None:
        end_date = pd.Timestamp.today().strftime('%Y-%m-%d')
        
    if market_index.startswith("TODO"):
        raise DataUnavailableError(market_index, country, [], "Market index is marked as TODO. Please update the config with a valid ticker.")
        
    bank_tickers = [b for b in bank_tickers if not b.startswith("TODO")]
    tickers = [market_index] + bank_tickers
    
    print(f"Fetching data for {len(tickers)} tickers from {start_date} to {end_date}...")
    
    chain = setup_fallback_chain()
    
    fetched_data = {}
    for ticker in tickers:
        print(f"  Attempting to fetch {ticker}...")
        df = chain.fetch_with_fallback(ticker, country, start_date, end_date, required_rows=min_rows, event_date=event_date)
        # Rename 'Close' to the ticker name for joining
        df = df.rename(columns={'Close': ticker})
        fetched_data[ticker] = df
        
    if not fetched_data:
        raise DataUnavailableError("All", country, [], "No tickers could be fetched.")
        
    # Join all DataFrames on the Date index
    combined_data = pd.concat(fetched_data.values(), axis=1)
    
    # Forward fill missing values to handle timezone/holiday mismatches between markets and banks
    combined_data = combined_data.ffill()
    
    # Calculate daily returns (percentage change)
    returns = combined_data.pct_change().dropna(how='all')
    
    if returns.empty or len(returns) < min_rows:
        raise DataUnavailableError(
            "Combined Returns", country, [], 
            f"After merging, insufficient overlapping valid return rows. Needed {min_rows}, got {len(returns)}."
        )
    
    # We no longer save to CSV to avoid side effects in the cached function
    # The cache handles storing this DataFrame directly in memory.
    print(f"\nTotal Trading Days Fetched: {len(returns)}")
    return returns

if __name__ == "__main__":
    # Fallback to US if run directly
    df = fetch_data_for_region('United States', '^GSPC', ['JPM', 'BAC'])
    print(df.head())
