
import yfinance as yf
import time
data=yf.download("RELIANCE.NS", period="5y", multi_level_index=False)
print(data)


def get_sma(closing_price,window):
    sma=   closing_price.rolling(window=window).mean()
    return sma
sma=get_sma(data['Close'],window=9)
sma

import pandas_ta_classic as ta

def get_ema(closing_price,window):
    ema=ta.ema(closing_price,window)
    return ema
ema=get_ema(data['Close'],window=9)
ema


from backtesting import Backtest, Strategy

class sma_strategy(Strategy):
    n1=50
    n2=20

    def init(self):
        self.sma1=self.I(get_sma,self.data.Close.s,self.n1)
        self.ema1=self.I(get_ema,self.data.Close.s,self.n2)

    def next(self):
        current_closing_price=self.data.Close[-1]
        previous_closing_price=self.data.Close[-2]
        current_sma=self.sma1[-1]
        previous_sma=self.sma1[-2]
        current_ema=self.ema1[-1]
        previous_ema=self.ema1[-2]

        if current_ema>current_sma and previous_sma>previous_ema:
            self.position.close()
            self.buy()
        elif current_ema<current_sma and previous_sma<previous_ema:
            self.position.close()
            self.sell()

b1=Backtest(data,sma_strategy,cash=10000)
result=b1.run()
b1.plot()
print(result)