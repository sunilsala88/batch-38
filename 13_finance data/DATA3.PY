import yfinance as yf
import numpy as np

# Reliance Industries on NSE -> ticker suffix is .NS
symbol = "RELIANCE.NS"
benchmark = "^NSEI"          # NIFTY 50, the index Reliance trades against

ticker = yf.Ticker(symbol)

# ---------------------------------------------------------------
# 1) Beta straight from Yahoo's key-statistics block.
#    Yahoo's number is 5 years of MONTHLY returns vs the S&P 500,
#    even for Indian stocks -- so treat it as a reference, not gospel.
# ---------------------------------------------------------------
info = ticker.info
print("Yahoo reported beta :", info.get("beta"))

# ---------------------------------------------------------------
# 2) Beta computed ourselves against the NIFTY 50.
#    beta = cov(stock_returns, index_returns) / var(index_returns)
# ---------------------------------------------------------------
px = yf.download([symbol, benchmark], period="5y", interval="1mo",
                 auto_adjust=True, progress=False)["Close"]

# monthly % change, drop the first NaN row and any month a series is missing
ret = px.pct_change().dropna()

cov = np.cov(ret[symbol], ret[benchmark])     # 2x2 covariance matrix
beta = cov[0, 1] / cov[1, 1]

print("Months used          :", len(ret))
print(f"Beta vs NIFTY 50     : {beta:.4f}")

# same thing via a least-squares fit: slope is beta, intercept is monthly alpha
slope, intercept = np.polyfit(ret[benchmark], ret[symbol], 1)
print(f"Beta  (regression)   : {slope:.4f}")
print(f"Alpha (monthly)      : {intercept:.4%}")
