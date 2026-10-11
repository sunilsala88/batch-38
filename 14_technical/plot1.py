import yfinance as yf
import mplfinance as mpf
import pandas_ta_classic as ta

df = yf.download("RELIANCE.NS", period="730d", interval="1h", multi_level_index=False)
print(df)

df['sma'] = df['Close'].rolling(20).mean()


# ---- same EMA with pandas_ta ----
# note: 'length', not 'timeperiod'. The returned Series is already named EMA_20.
df['ema_pta'] = ta.ema(df['Close'], length=20)

# accessor style -- pandas_ta adds a .ta on every DataFrame and finds the
# 'Close' column by itself, so you don't pass the series in
df['ema_pta_50'] = df.ta.ema(length=50)

print(df)


# ======================================================================
# indicators for the chart
# ======================================================================
# bbands returns 5 columns: lower / mid / upper, plus bandwidth and %B.
# The names carry the settings, so length=20 std=2 -> BBL_20_2.0 etc.
bb = ta.bbands(df['Close'], length=20, std=2)
df['bb_low'] = bb['BBL_20_2.0']
df['bb_up'] = bb['BBU_20_2.0']

df['rsi'] = ta.rsi(df['Close'], length=14)

# macd returns the line, the histogram (h) and the signal (s)
macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
df['macd'] = macd['MACD_12_26_9']
df['macd_signal'] = macd['MACDs_12_26_9']
df['macd_hist'] = macd['MACDh_12_26_9']


# ======================================================================
# plotting
# ======================================================================
# 730 days of hourly bars is ~3,600 candles. Drawn all at once each candle is
# thinner than a pixel and the chart is a grey smear -- so always plot a window.
# The indicators above were computed on the FULL history, then sliced, so the
# EMA-50 at the left edge still knows about the 50 bars before it.
BARS = 150
plot_df = df.tail(BARS)

# One color per job, assigned in a fixed order -- not cycled per run.
UP, DOWN = '#008300', '#e34948'      # candle bodies: the domain convention
EMA_20, EMA_50 = '#2a78d6', '#c98500'  # amber, not orange -- see note below
BAND = '#9a9890'                     # bands are context, so keep them recessive
# EMA 50 is amber rather than orange deliberately: an orange line lands on top
# of the red down-candles it shares the panel with, and the two are hard to
# tell apart even with full colour vision.
GRID = '#dddcd6'

mc = mpf.make_marketcolors(
    up=UP, down=DOWN,
    edge={'up': UP, 'down': DOWN},
    wick={'up': UP, 'down': DOWN},
    volume={'up': UP, 'down': DOWN},
)
style = mpf.make_mpf_style(
    marketcolors=mc,
    facecolor='#fcfcfb',
    figcolor='#fcfcfb',
    gridcolor=GRID,
    gridstyle='-',
    rc={'axes.edgecolor': GRID, 'axes.labelcolor': '#52514e',
        'xtick.color': '#52514e', 'ytick.color': '#52514e',
        'font.size': 9},
)

# Every extra series is an addplot. `panel=0` draws on the candle axes;
# panel 1 is the volume, so the oscillators go on panels 2 and 3.
# Each oscillator gets its OWN panel rather than a second y-axis on the price
# chart -- two scales on one axes can be made to show any relationship you like.
extras = [
    mpf.make_addplot(plot_df['ema_pta'], panel=0, secondary_y=False, color=EMA_20, width=1.4, label='EMA 20'),
    mpf.make_addplot(plot_df['ema_pta_50'], panel=0, secondary_y=False, color=EMA_50, width=1.4, label='EMA 50'),
    mpf.make_addplot(plot_df['bb_up'], panel=0, secondary_y=False, color=BAND, width=1.0, linestyle='--', label='Bollinger 20/2'),
    mpf.make_addplot(plot_df['bb_low'], panel=0, secondary_y=False, color=BAND, width=1.0, linestyle='--'),

    # RSI is bounded 0-100, so pin the scale instead of letting it auto-fit --
    # otherwise 30 and 70 drift around and stop meaning anything at a glance
    mpf.make_addplot(plot_df['rsi'], panel=2, secondary_y=False, color='#4a3aa7',
                     width=1.4, ylabel='RSI 14', ylim=(0, 100)),
    # 70/30 as flat reference lines: a Series of one repeated value
    mpf.make_addplot(plot_df['rsi'] * 0 + 70, panel=2, secondary_y=False, color=BAND, width=0.9, linestyle=':'),
    mpf.make_addplot(plot_df['rsi'] * 0 + 30, panel=2, secondary_y=False, color=BAND, width=0.9, linestyle=':'),

    mpf.make_addplot(plot_df['macd_hist'], panel=3, secondary_y=False, type='bar', width=0.7,
                     color=[UP if v >= 0 else DOWN for v in plot_df['macd_hist']],
                     alpha=0.55, ylabel='MACD'),
    mpf.make_addplot(plot_df['macd'], panel=3, secondary_y=False, color=EMA_20, width=1.4),
    mpf.make_addplot(plot_df['macd_signal'], panel=3, secondary_y=False, color=EMA_50, width=1.4),
]

fig, axes = mpf.plot(
    plot_df,
    type='candle',
    style=style,
    addplot=extras,
    volume=True,
    # panel 0 is price and gets the room; the rest are supporting detail
    panel_ratios=(6, 1.4, 2, 2),
    figsize=(14, 10),
    ylabel='Price',
    ylabel_lower='Volume',
    returnfig=True,   # hand back fig/axes so we can add the legend ourselves
)

# mplfinance draws no legend on its own, and with four overlays on the price
# panel the colors alone don't say which line is which.
axes[0].legend(loc='upper left', fontsize=8, frameon=False)

# set the title on the figure, not via mpf's `title=` -- that one gets pulled
# down into the price axes and lands on top of the candles
fig.suptitle(f'RELIANCE.NS  1h  (last {BARS} bars)', x=0.06, y=0.97,
             ha='left', fontsize=13, color='#0b0b0b')


fig.savefig('reliance_candles.png', dpi=130)
mpf.show()
