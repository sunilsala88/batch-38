import yfinance as yf
import talib
import pandas_ta_classic as ta

df = yf.download("RELIANCE.NS", period="730d", interval="1h", multi_level_index=False)
print(df)

df['sma'] = df['Close'].rolling(20).mean()

# ---- EMA with talib ----
# talib.EMA needs a float64 series -- it returns a Series with the same index,
# NaN for the first (timeperiod - 1) rows because there isn't enough history yet.
df['ema'] = talib.EMA(df['Close'], timeperiod=20)

df['ema_50'] = talib.EMA(df['Close'], timeperiod=50)
df['ema_200'] = talib.EMA(df['Close'], timeperiod=200)

# ---- same EMA with pandas_ta ----
# note: 'length', not 'timeperiod'. The returned Series is already named EMA_20.
df['ema_pta'] = ta.ema(df['Close'], length=20)

# accessor style -- pandas_ta adds a .ta on every DataFrame and finds the
# 'Close' column by itself, so you don't pass the series in
df['ema_pta_50'] = df.ta.ema(length=50)

# both libraries agree (difference is float rounding, ~1e-13)
print((df['ema'] - df['ema_pta']).abs().max())

print(df[['Close', 'sma', 'ema', 'ema_pta', 'ema_50', 'ema_pta_50']].tail(10))
