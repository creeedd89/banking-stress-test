import pandas as pd
from abc import ABC, abstractmethod

class DataUnavailableError(Exception):
    def __init__(self, ticker, country, sources_tried, message=""):
        self.ticker = ticker
        self.country = country
        self.sources_tried = sources_tried
        self.message = message
        super().__init__(f"Data unavailable for {ticker} ({country}). Sources tried: {', '.join(sources_tried)}. {message}")

class MarketDataSource(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    def fetch(self, ticker: str, start: str, end: str) -> pd.DataFrame:
        """
        Fetches historical data for a ticker. 
        Returns a pd.DataFrame with a DatetimeIndex and at least a 'Close' column.
        Should return an empty DataFrame or raise an Exception on failure.
        """
        pass
