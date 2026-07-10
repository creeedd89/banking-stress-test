import pandas as pd
import os
from .base import MarketDataSource

class LocalCSVSource(MarketDataSource):
    @property
    def name(self) -> str:
        return "local_csv"
        
    def fetch(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """
        Attempts to read from 'data/cache/{ticker}.csv'
        Assumes the CSV has a 'Date' column and a 'Close' column.
        """
        try:
            # Clean up ticker string for filesystem
            safe_ticker = ticker.replace("^", "").replace(".", "_")
            filepath = os.path.join("data", "cache", f"{safe_ticker}.csv")
            
            if not os.path.exists(filepath):
                return pd.DataFrame()
                
            df = pd.read_csv(filepath, index_col='Date', parse_dates=True)
            
            if df.empty or 'Close' not in df.columns:
                return pd.DataFrame()
                
            # Filter by date range
            start_date = pd.to_datetime(start)
            end_date = pd.to_datetime(end)
            
            df = df.loc[(df.index >= start_date) & (df.index <= end_date)]
            
            df = df[['Close']]
            return df
        except Exception as e:
            print(f"Local CSV error for {ticker}: {e}")
            return pd.DataFrame()
