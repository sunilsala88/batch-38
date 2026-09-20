import datetime as dt

import pandas as pd
import yfinance as yf

# Reliance Industries on NSE -> ticker suffix is .NS
symbol = "RELIANCE.NS"

# Yahoo limits 1m data to the last 30 days, and only 7 days per request.
# So we walk backwards in 7-day windows and stitch the pieces together.
# (period="max" does NOT work here -- it silently returns fewer rows.)
end = dt.date.today() + dt.timedelta(days=1)
start = end - dt.timedelta(days=30)

parts = []
window_start = start
while window_start < end:
    window_end = min(window_start + dt.timedelta(days=7), end)

    chunk = yf.download(symbol, start=window_start, end=window_end,
                        interval="1m", auto_adjust=False, progress=False)

    # a window with no trading days (weekend/holiday) comes back empty
    if not chunk.empty:
        parts.append(chunk)

    window_start = window_end

df = pd.concat(parts)
df.columns = df.columns.droplevel(1)          # drop the ticker level
df = df[~df.index.duplicated(keep="first")]   # windows can overlap at the edges
df = df.sort_index()

df.index.name = "Date"      # yfinance calls it "Datetime" for intraday
df.columns.name = None      # drop the leftover "Price" axis label

print(df.head())
print(df.tail())
print(df.shape)
print(df)

df.to_csv("reliance_1m_max.csv")
