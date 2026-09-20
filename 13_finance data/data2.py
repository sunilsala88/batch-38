import yfinance as yf

# Reliance Industries on NSE -> ticker suffix is .NS
symbol = "HDFCBANK.NS"

ticker = yf.Ticker(symbol)

# Quarterly balance sheet.
# Line items come back as ROWS and reporting dates as COLUMNS (newest first),
# which is how a balance sheet is normally read.
bs = ticker.quarterly_balance_sheet

bs.index.name = "Item"
bs.columns.name = "Period"

print(bs.shape)
print(bs.columns.tolist())
print(bs.head(10))

# a few line items people usually want
wanted = ["Total Assets", "Total Debt", "Cash And Cash Equivalents",
          "Common Stock Equity", "Working Capital"]
print(bs.loc[[i for i in wanted if i in bs.index]])

bs.to_csv("reliance_quarterly_balance_sheet.csv")
