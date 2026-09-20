import yfinance as yf

# Reliance Industries on NSE -> ticker suffix is .NS
symbol = "RELIANCE.NS"

# Max available 1h history.
# Use period="730d" -- NOT "max". Yahoo passes "730d" straight through as a
# native range and returns ~1070 days of bars, while "max" gets converted to
# start/end timestamps and comes back with only ~725 days.
# Anything larger ("1000d", "5y") trips Yahoo's 730-day intraday guard and
# returns nothing at all.
df = yf.download(symbol, period="730d", interval="1h",
                 auto_adjust=False, progress=False)

df.columns = df.columns.droplevel(1)          # drop the ticker level

df.index.name = "Date"      # yfinance calls it "Datetime" for intraday
df.columns.name = None      # drop the leftover "Price" axis label

print(df.head())
print(df.tail())
print(df.shape)
print(df)
df.to_csv("reliance_1h_max.csv")
