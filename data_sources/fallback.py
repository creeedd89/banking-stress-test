import pandas as pd
from typing import List
from .base import MarketDataSource, DataUnavailableError

class FallbackChain:
    def __init__(self, sources: List[MarketDataSource]):
        self.sources = sources
        
    def fetch_with_fallback(self, ticker: str, country: str, start: str, end: str, required_rows: int = 0, event_date: str = None) -> pd.DataFrame:
        """
        Tries each data source in order. 
        Returns the first DataFrame that meets the criteria:
        - Non-empty
        - No NaN-only columns
        - Sufficient rows (>= required_rows)
        - Covers event_date if provided
        Raises DataUnavailableError if all sources fail.
        """
        sources_tried = []
        
        for source in self.sources:
            sources_tried.append(source.name)
            df = source.fetch(ticker, start, end)
            
            if df is not None and not df.empty:
                # 1. Check for all NaN columns
                if df.isnull().all().any():
                    print(f"WARNING: {source.name} returned NaN-only columns for {ticker}.")
                    continue
                
                # 2. Check required rows
                if len(df) < required_rows:
                    print(f"WARNING: {source.name} returned insufficient data for {ticker}. Expected {required_rows}, got {len(df)}.")
                    continue
                
                # 3. Check event date coverage
                if event_date:
                    evt_dt = pd.to_datetime(event_date)
                    min_dt = df.index.min()
                    max_dt = df.index.max()
                    
                    # We allow a margin of 14 days to be "reasonably close" in case of holidays/weekends or data gaps
                    margin = pd.Timedelta(days=14)
                    if evt_dt < (min_dt - margin) or evt_dt > (max_dt + margin):
                        print(f"WARNING: {source.name} data for {ticker} does not cover event date {event_date}. Date range: {min_dt.date()} to {max_dt.date()}")
                        continue
                
                print(f"SUCCESS: Fetched {ticker} using {source.name} (Rows: {len(df)})")
                return df
            else:
                print(f"FAILED: {source.name} failed or returned empty data for {ticker}.")
                
        # If we reached here, all sources failed
        raise DataUnavailableError(
            ticker=ticker,
            country=country,
            sources_tried=sources_tried,
            message=f"Could not fetch {required_rows} valid trading days for {ticker} covering event date {event_date}."
        )
