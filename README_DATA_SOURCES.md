# 🌐 Multi-Source Data Architecture

The `banking-stress-test` uses a robust **Chain of Responsibility** fallback architecture for fetching historical market data. Because different financial APIs have varying coverage for emerging and frontier markets, this architecture ensures that if one source fails, it seamlessly falls back to another, rather than crashing the pipeline.

## 📦 Available Data Sources

The abstraction layer lives in the `data_sources/` package. Currently supported sources are prioritized in this order:

1. **`YFinanceSource` (`yfinance`)**: The default engine. Fast and reliable for US, EU, and major Asian markets. Can occasionally fail or return truncated data for frontier markets due to timezone bugs.
2. **`StooqSource` (`stooq`)**: The first fallback. A free historical data provider that excels at global indices and European/Asian equities. Queries via `https://stooq.com/q/d/l/`.
3. **`LocalCSVSource` (`local_csv`)**: The ultimate fallback. Reads static CSV files from the `data/cache/` directory.

## ⚙️ How the Fallback Chain Works

When the app requests data (e.g., for `PAK` and `HBL`), the `FallbackChain` in `fetch_data.py`:
1. Skips any placeholder tickers prefixed with `TODO_` as defined in `markets.yaml`.
2. Asks `YFinanceSource` for the `PAK` data. If it returns successfully, has enough rows (based on the user's `Estimation Window`), and covers the event date, it stops and returns.
3. If `YFinance` fails (or returns an empty dataframe/insufficient rows), it asks `StooqSource`.
4. If `Stooq` fails, it asks `LocalCSVSource`.
5. If *all* sources fail, it raises a strict `DataUnavailableError` which `app.py` catches to display a clean, graceful error message in the Streamlit UI, preventing raw Python `IndexError` stack traces.

## 🗺️ Adding a New Country or Market

To add a new market to the UI, you only need to edit `markets.yaml`. No code changes are required!

```yaml
Africa:
  Egypt:
    index_ticker: "EGPT"
    preferred_source: "yfinance"
    banks:
      COMI: "COMI.CA"
    events:
      - name: "2020 COVID Crash"
        date: "2020-03-09"
        category: "Force Majeure"
        description: "COVID crash hitting Egyptian equities."
```
Once added to `markets.yaml`, it will automatically appear in the Streamlit sidebar.

## 🛠️ Adding a Custom Data Source

To add a new provider (e.g., AlphaVantage, EODHD, Investpy), you do **not** need to touch the frontend or the event study logic.

1. Create a new file in `data_sources/` (e.g., `alphavantage_source.py`).
2. Inherit from `MarketDataSource` and implement the `fetch()` method:
    ```python
    import pandas as pd
    from .base import MarketDataSource

    class AlphaVantageSource(MarketDataSource):
        @property
        def name(self) -> str:
            return "alpha_vantage"
            
        def fetch(self, ticker: str, start: str, end: str) -> pd.DataFrame:
            # Your API logic here...
            # Must return a DataFrame with a DatetimeIndex and a 'Close' column
            return df
    ```
3. Open `fetch_data.py` and register it in the `setup_fallback_chain()` function:
    ```python
    from data_sources.alphavantage_source import AlphaVantageSource
    
    def setup_fallback_chain() -> FallbackChain:
        return FallbackChain([
            YFinanceSource(),
            AlphaVantageSource(), # <-- Add it here!
            StooqSource(),
            LocalCSVSource()
        ])
    ```

## 🗃️ Local CSV Fallback

If an emerging market ticker is not covered by *any* API, you can manually upload it:
1. Download historical daily data for the ticker.
2. Ensure the CSV has a `Date` column (formatted `YYYY-MM-DD`) and a `Close` column.
3. Name the file `{ticker}.csv`.
   * *Note: Strip out `^` and replace `.` with `_`. For example, `^KSE100` becomes `KSE100.csv`, and `HBL.KAR` becomes `HBL_KAR.csv`.*
4. Place the file in the `/data/cache/` folder (create the folder if it doesn't exist).
5. The `LocalCSVSource` will automatically find and parse it!
