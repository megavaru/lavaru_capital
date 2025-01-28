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
```
---

### Notes
- The function uses the CCXT library to interact with the exchange's API.
- Data is fetched in batches of 500 rows per request to avoid API limits.
- The timestamp column is converted to a datetime index for easier time-based analysis.

---

## `resample_data` Function

### Description
Resamples OHLCV (Open, High, Low, Close, Volume) data to a different timeframe using pandas. This function is useful for converting data from a smaller timeframe (e.g., 1-minute) to a larger one (e.g., 1-hour or 1-day).

---

### Parameters
| Parameter        | Type           | Description                                                                 |
|------------------|----------------|-----------------------------------------------------------------------------|
| `data`           | `pd.DataFrame` | The input OHLCV data with a datetime index. Must include columns: `open`, `high`, `low`, `close`, `volume`. |
| `timeframe`      | `str`          | The target timeframe for resampling. Supported values: `"15min"`, `"30min"`, `"1h"`, `"4h"`, `"1d"`, `"1w"`, `"1ME"`. |

---

### Returns
- **`resampled_data`** (`pd.DataFrame`): The resampled OHLCV data with the following columns:
  - `open`: The opening price of the new candle.
  - `high`: The highest price of the new candle.
  - `low`: The lowest price of the new candle.
  - `close`: The closing price of the new candle.
  - `volume`: The total volume of the new candle.

---

### Supported Timeframes
| Timeframe | Description          |
|-----------|----------------------|
| `"15min"` | 15-minute candles    |
| `"30min"` | 30-minute candles    |
| `"1h"`    | 1-hour candles       |
| `"4h"`    | 4-hour candles       |
| `"1d"`    | 1-day candles        |
| `"1w"`    | 1-week candles       |
| `"1ME"`   | 1-month candles      |

---

### Example Usage
```python
# Fetch 1-minute OHLCV data for BTC/USDT from Binance
data = get_data(symbol="BTC/USDT", timeframe="1m", start_date="2025-01-20T00:00:00Z")

# Resample the data to 1-hour timeframe
resampled_data = resample_data(data, timeframe="1h")

# Print the resampled data
print(resampled_data.head())
