from tradingview_screener import Query, col

# 'SYML:NSE;NIFTY' = the Nifty 50 index. set_index() picks the universe for us,
# so no set_markets('india') here -- calling set_markets AFTER set_index is a 400 error.
count, df = (Query()
    .set_index('SYML:NSE;NIFTY')
    .select('name', 'close', 'volume', 'market_cap_basic', 'price_earnings_ttm', 'RSI')
    .where(col('price_earnings_ttm') >= 50)
              
    .order_by('volume', ascending=False)
    .limit(50)
    .get_scanner_data())

# count = total stocks matching the filters, df = the rows we asked for (limit 50)
print(count)
print(df)
