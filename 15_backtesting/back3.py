import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta_classic as ta

data=yf.download("RELIANCE.NS", period="2y", multi_level_index=False)
print(data)


def get_atr(data,period):
    high_low=data['High']-data['Low']
    high_close=(data['High']-data['Close'].shift(1)).abs()
    low_close=(data['Low']-data['Close'].shift(1)).abs()
    tr=pd.concat([high_low,high_close,low_close],axis=1).max(axis=1)
    # Wilder's smoothing (same as RMA used on TradingView)
    atr=tr.ewm(alpha=1/period,adjust=False).mean()
    return atr


def get_supertrend(data,period=10,multiplier=3):
    high=data['High'].values
    low=data['Low'].values
    close=data['Close'].values
    atr=get_atr(data,period).values

    hl2=(high+low)/2
    basic_upper=hl2+multiplier*atr
    basic_lower=hl2-multiplier*atr

    n=len(data)
    final_upper=np.zeros(n)
    final_lower=np.zeros(n)
    supertrend=np.full(n,np.nan)
    direction=np.ones(n)   # 1 = uptrend, -1 = downtrend

    final_upper[0]=basic_upper[0]
    final_lower[0]=basic_lower[0]

    for i in range(1,n):
        # upper band only moves down, unless price closed above it
        if basic_upper[i]<final_upper[i-1] or close[i-1]>final_upper[i-1]:
            final_upper[i]=basic_upper[i]
        else:
            final_upper[i]=final_upper[i-1]

        # lower band only moves up, unless price closed below it
        if basic_lower[i]>final_lower[i-1] or close[i-1]<final_lower[i-1]:
            final_lower[i]=basic_lower[i]
        else:
            final_lower[i]=final_lower[i-1]

        # trend flips when close crosses the opposite band
        if close[i]>final_upper[i-1]:
            direction[i]=1
        elif close[i]<final_lower[i-1]:
            direction[i]=-1
        else:
            direction[i]=direction[i-1]

        supertrend[i]=final_lower[i] if direction[i]==1 else final_upper[i]

    # first `period` values are not reliable while ATR warms up
    supertrend[:period]=np.nan
    return pd.Series(supertrend,index=data.index),pd.Series(direction,index=data.index)


data['supertrend'],data['direction']=get_supertrend(data,period=10,multiplier=3)
data['signal']=data['direction'].diff()   # 2 = buy (flip to up), -2 = sell (flip to down)
print(data[['Close','supertrend','direction','signal']].tail(20))

print('buy signals')
print(data[data['signal']==2][['Close','supertrend']])
print('sell signals')
print(data[data['signal']==-2][['Close','supertrend']])


# cross-check with pandas_ta_classic
st=ta.supertrend(data['High'],data['Low'],data['Close'],length=10,multiplier=3)
print(st.tail(10))



from backtesting import Backtest, Strategy

def get_ema(closing_price,window):
    ema=ta.ema(closing_price,window)
    return ema

def get_supertrend_line(df,period,multiplier):
    supertrend,direction=get_supertrend(df,period,multiplier)
    return supertrend

def get_supertrend_direction(df,period,multiplier):
    supertrend,direction=get_supertrend(df,period,multiplier)
    return direction


class ema_supertrend_strategy(Strategy):
    ema_period=50
    st_period=10
    st_multiplier=3

    def init(self):
        self.ema1=self.I(get_ema,self.data.Close.s,self.ema_period)
        self.st=self.I(get_supertrend_line,self.data.df,self.st_period,self.st_multiplier,overlay=True)
        self.st_dir=self.I(get_supertrend_direction,self.data.df,self.st_period,self.st_multiplier,overlay=False)

    def next(self):
        current_closing_price=self.data.Close[-1]
        current_ema=self.ema1[-1]
        current_direction=self.st_dir[-1]

        # entry: supertrend positive (uptrend) and close above ema
        if not self.position and current_direction==1 and current_closing_price>current_ema:
            self.buy()
        # exit: close below ema
        elif self.position and current_closing_price<current_ema:
            self.position.close()


b1=Backtest(data,ema_supertrend_strategy,cash=10000,commission=0.001)
result=b1.run()
b1.plot()
print(result)
print(result['_trades'])
