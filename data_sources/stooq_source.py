import pandas as pd
import requests
import io
from .base import MarketDataSource

class StooqSource(MarketDataSource):
    @property
    def name(self) -> str:
        return "stooq"
        
    def fetch(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """
        Fetches data from stooq.com CSV API.
        Example URL: https://stooq.com/q/d/l/?s={ticker}&d1={start}&d2={end}&i=d
        Note: Stooq dates are formatted as YYYYMMDD
        """
        try:
            start_formatted = start.replace("-", "")
            end_formatted = end.replace("-", "")
            
            # Use lower case for standard stooq tickers, although it's often case-insensitive
            # If the config specifies a .US or .UK extension, stooq usually handles it.
            # E.g., ^SPX, AAPL.US
            url = f"https://stooq.com/q/d/l/?s={ticker}&d1={start_formatted}&d2={end_formatted}&i=d"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                return pd.DataFrame()
                
            # Stooq returns text "Exceeded the daily limit" if blocked, or empty content if missing
            text = response.text
            if "Exceeded" in text or "No data" in text or len(text.strip()) == 0:
                return pd.DataFrame()
                
            df = pd.read_csv(io.StringIO(text), index_col='Date', parse_dates=True)
            
            if df.empty or 'Close' not in df.columns:
                return pd.DataFrame()
                
            # Keep only the Close column
            df = df[['Close']]
            
            # Ensure it is sorted chronologically
            df = df.sort_index()
            
            return df
        except Exception as e:
            print(f"Stooq error for {ticker}: {e}")
            return pd.DataFrame()
