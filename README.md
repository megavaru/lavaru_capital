## `get_data` Function

### Description
Fetches OHLCV (Open, High, Low, Close, Volume) data for a given trading symbol and timeframe using the [CCXT](https://github.com/ccxt/ccxt) library. The data is retrieved from a specified exchange and returned as a pandas DataFrame.

---

### Parameters
| Parameter        | Type      | Default Value           | Description                                                                 |
|------------------|-----------|-------------------------|-----------------------------------------------------------------------------|
| `symbol`         | `str`     | **Required**            | The trading symbol (e.g., `"BTC/USDT"`).                                    |
| `timeframe`      | `str`     | `"1h"`                  | The timeframe for the OHLCV data (e.g., `"1h"` for 1-hour candles).         |
| `start_date`     | `str`     | `"2024-01-01T00:00:00Z"`| The start date for the data in ISO 8601 format.                             |
| `end_date`       | `str`     | `None`                  | The end date for the data in ISO 8601 format. If `None`, uses current UTC.  |
| `exchange_name`  | `str`     | `"binance"`             | The name of the exchange (e.g., `"binance"`).                               |
| `delay`          | `float`   | `0.1`                   | Delay (in seconds) between API requests to avoid rate limits.               |

---

### Returns
- **`df`** (`pd.DataFrame`): A pandas DataFrame containing the OHLCV data with the following columns:
  - `timestamp`: The timestamp of the candle (as a datetime index).
  - `open`: The opening price.
  - `high`: The highest price.
  - `low`: The lowest price.
  - `close`: The closing price.
  - `volume`: The trading volume.

---

### Example Usage
```python
# Fetch 1-hour OHLCV data for BTC/USDT from Binance
data = get_data(symbol="BTC/USDT", timeframe="1h", start_date="2024-01-01T00:00:00Z")
print(data.head())
