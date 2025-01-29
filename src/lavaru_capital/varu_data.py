import ccxt
import pandas as pd
from datetime import datetime
import time
import pandas_ta as ta
import numpy as np

#### Get data function ####

def get_data(
    symbol: str,
    timeframe: str = "1h",
    start_date: str = "2024-01-01T00:00:00Z",
    end_date: str = None,
    exchange_name: str = "binance",
    delay: float = 0.1,
) -> None:
    """
    Fetch OHLCV data for a given symbol and timeframe using CCXT.
    """
    # Initialize the exchange
    exchange = getattr(ccxt, exchange_name)()

    # Set end_date to current UTC time if not provided
    if end_date is None:
        end_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Convert start and end dates to timestamps
    since = exchange.parse8601(start_date)
    until = exchange.parse8601(end_date)

    # List to store all OHLCV data
    all_ohlcv = []

    # Fetch OHLCV data in batches (max 500 rows per request)
    while since < until:
        # Fetch OHLCV data (max 500 rows per request)
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since, limit=500)

        # If no data is returned, break the loop
        if not ohlcv:
            break

        # Append the data to the list
        all_ohlcv += ohlcv

        # Update the `since` parameter to the timestamp of the last candle + 1ms
        since = ohlcv[-1][0] + 1

        # Sleep to avoid hitting rate limits
        time.sleep(delay)

    # Convert to a pandas DataFrame
    df = pd.DataFrame(all_ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")  # Convert timestamp to datetime
    df.set_index("timestamp", inplace=True)  # Set timestamp as the index
    
    # Ensure the DataFrame is sorted by time
    df = df.sort_index()

    # Print the DataFrame
    return df

#### Resampling function ####

def resample_data(data: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """
    Resample OHLCV data to a different timeframe.

    Supported timeframes:
    - "15min": 15 minutes
    - "30min": 30 minutes
    - "1h": 1 hour
    - "4h": 4 hours
    - "1d": 1 day
    - "1w": 1 week
    - "1ME": 1 month

    Parameters:
        data (pd.DataFrame): The input OHLCV data with a datetime index.
        timeframe (str): The target timeframe (e.g., "15min", "1h", "1d").

    Returns:
        pd.DataFrame: The resampled OHLCV data.
    """
    # Define the aggregation rules for OHLCV
    aggregation_rules = {
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }

    # Resample the data
    resampled_data = data.resample(timeframe).apply(aggregation_rules).dropna()

    return resampled_data

#### Indicators function ####

def add_indicators(
    df: pd.DataFrame,
    length: int = 14,  # Default length for all indicators
    sma_length: int = None,  # Specific length for SMA
    ema_length: int = None,  # Specific length for EMA
    atr_length: int = None,  # Specific length for ATR
    adx_length: int = None,  # Specific length for ADX
    cci_length: int = None,  # Specific length for CCI
    roc_length: int = None,  # Specific length for ROC
    willr_length: int = None,  # Specific length for Williams %R
    cmf_length: int = None,  # Specific length for CMF
    vwma_length: int = None,  # Specific length for VWMA
) -> pd.DataFrame:
    """
    Add technical indicators to the DataFrame.
    If `length` is set, it will be used as the default length for all indicators.
    If a specific indicator length is set (e.g., `vwma_length`), it will override the default length.
    """
    # Ensure the DataFrame is sorted by time
    df = df.sort_index()

    # Helper function to choose the length
    def get_length(default_length, specific_length):
        return specific_length if specific_length is not None else default_length

    # Calculate EMA (Exponential Moving Average)
    ema_len = get_length(length, ema_length)
    df[f'EMA_{ema_len}'] = df['close'].ewm(span=ema_len, adjust=False).mean()

    # Calculate SMA (Simple Moving Average)
    sma_len = get_length(length, sma_length)
    df[f'SMA_{sma_len}'] = df['close'].rolling(window=sma_len).mean()

    # Calculate RSI (Relative Strength Index)
    rsi_len = get_length(length, length)  # RSI uses the default `length`
    df[f'RSI_{rsi_len}'] = ta.rsi(df['close'], length=rsi_len)

    # Calculate ATR (Average True Range)
    atr_len = get_length(length, atr_length)
    df[f'ATR_{atr_len}'] = ta.atr(df['high'], df['low'], df['close'], length=atr_len)

    # Calculate VWAP (Volume Weighted Average Price)
    df['VWAP'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'])

    # Calculate ADX (Average Directional Index)
    adx_len = get_length(length, adx_length)
    adx_result = ta.adx(df['high'], df['low'], df['close'], length=adx_len)
    df[f'ADX_{adx_len}'] = adx_result[f'ADX_{adx_len}']

    # Calculate CCI (Commodity Channel Index)
    cci_len = get_length(length, cci_length)
    df[f'CCI_{cci_len}'] = ta.cci(df['high'], df['low'], df['close'], length=cci_len)

    # Calculate OBV (On-Balance Volume)
    df['OBV'] = ta.obv(df['close'], df['volume'])

    # Calculate ROC (Rate of Change)
    roc_len = get_length(length, roc_length)
    df[f'ROC_{roc_len}'] = ta.roc(df['close'], length=roc_len)

    # Calculate Williams %R
    willr_len = get_length(length, willr_length)
    df[f'Williams_%R_{willr_len}'] = ta.willr(df['high'], df['low'], df['close'], length=willr_len)

    # Calculate CMF (Chaikin Money Flow)
    cmf_len = get_length(length, cmf_length)
    df[f'CMF_{cmf_len}'] = ta.cmf(df['high'], df['low'], df['close'], df['volume'], length=cmf_len)

    # Calculate VWMA (Volume Weighted Moving Average)
    vwma_len = get_length(length, vwma_length)
    df[f'VWMA_{vwma_len}'] = ta.vwma(df['close'], df['volume'], length=vwma_len)

    return df

#### Hawkes process function ####

def varu_hawkes(data: pd.Series, kappa: float):
    assert(kappa > 0.0)
    alpha = np.exp(-kappa)
    arr = data.to_numpy()
    output = np.zeros(len(data))
    output[:] = np.nan
    for i in range(1, len(data)):
        if np.isnan(output[i - 1]):
            output[i] = arr[i]
        else:
            output[i] = output[i - 1] * alpha + arr[i]
    return pd.Series(output, index=data.index) * kappa
