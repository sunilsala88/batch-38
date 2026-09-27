from finvizfinance.quote import finvizfinance

stock = finvizfinance('tsla')

stock_fundament = stock.ticker_fundament()
print(stock_fundament)
# result
# stock_fundament = {'Company': 'Tesla, Inc.', 'Sector': 'Consumer Cyclical',
# 'Industry': 'Auto Manufacturers', 'Country': 'USA', 'Index': '-', 'P/E': '849.57',
# 'EPS (ttm)': '1.94', 'Insider Own': '0.10%', 'Shs Outstand': '186.00M',
# 'Perf Week': '13.63%', 'Market Cap': '302.10B', 'Forward P/E': '106.17',
# ...}

from finvizfinance.screener.overview import Overview

foverview = Overview()
filters_dict = {'Index':'S&P 500','Sector':'Basic Materials','Dividend Yield':'High (>5%)'}
foverview.set_filter(filters_dict=filters_dict)
df = foverview.screener_view()
print(df)

# Descriptive filters: Exchange = NASDAQ, Index = DJIA, Sector = Technology
foverview = Overview()
filters_dict = {
    'Exchange': 'NASDAQ',
    'Index': 'DJIA',
    'Sector': 'Technology',
}
foverview.set_filter(filters_dict=filters_dict)
# Order by Ticker, ascending (same as the screener's default sort)
df = foverview.screener_view(order='Ticker', ascend=True)
print(df)
