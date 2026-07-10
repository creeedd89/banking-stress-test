import yfinance as yf
import pandas as pd
from .base import MarketDataSource

class YFinanceSource(MarketDataSource):
    @property
    def name(self) -> str:
        return "yfinance"
        
    def fetch(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        try:
            # yfinance expects string dates in 'YYYY-MM-DD'
            data = yf.download(ticker, start=start, end=end, progress=False)
            if data.empty:
                return pd.DataFrame()
            
            # yf.download can return multi-index columns if multiple tickers, 
            # but we fetch one by one in the new architecture
            if isinstance(data.columns, pd.MultiIndex):
                # Flatten or select the ticker
                if ticker in data.columns.get_level_values(1):
                    df = data.xs(ticker, level=1, axis=1)
                else:
                    df = data
            else:
                df = data
                
            if 'Close' not in df.columns:
                return pd.DataFrame()
                
            # Keep only the Close column to match our interface expectation
            df = df[['Close']]
            return df
        except Exception as e:
            print(f"YFinance error for {ticker}: {e}")
            return pd.DataFrame()
