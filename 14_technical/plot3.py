# Same chart again, this time with TradingView's own charting library.
#
# "TradingView" in Python means the `lightweight-charts` package, which wraps
# TradingView's open-source Lightweight Charts (the engine behind their site).
#   pip install lightweight-charts
#
# Unlike plot1 (a PNG) and plot2 (an HTML page), this one opens a native desktop
# window with the real TradingView feel: crosshair, snapping legend, wheel zoom,
# drag to pan. Closing the window ends the script.
import yfinance as yf
import pandas_ta_classic as ta
from lightweight_charts import Chart

df = yf.download("RELIANCE.NS", period="730d", interval="1h", multi_level_index=False)

# ---- indicators (computed on the FULL history, sliced afterwards) ----
df['EMA 20'] = ta.ema(df['Close'], length=20)
df['EMA 50'] = ta.ema(df['Close'], length=50)

bb = ta.bbands(df['Close'], length=20, std=2)
df['BB upper'] = bb['BBU_20_2.0']
df['BB lower'] = bb['BBL_20_2.0']

df['RSI 14'] = ta.rsi(df['Close'], length=14)

macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
df['MACD'] = macd['MACD_12_26_9']
df['Signal'] = macd['MACDs_12_26_9']
df['Histogram'] = macd['MACDh_12_26_9']

BARS = 150
plot_df = df.tail(BARS).copy()

# ---- shape the frame the way lightweight-charts wants it ----
# It looks for a 'date' (or 'time') COLUMN, not an index, and lowercase
# open/high/low/close/volume. yfinance gives us a tz-aware index (+05:30);
# the JS side wants naive timestamps, so drop the tz after slicing.
#
# The .astype('datetime64[ns]') is NOT cosmetic. Internally the library does
#     df['time'].astype('int64') // 10**9
# to reach epoch seconds, which only works on nanosecond datetimes. yfinance
# now returns SECOND resolution, where astype('int64') is already seconds --
# the extra //10**9 then collapses every bar to time=1 and the whole series
# lands on a single x coordinate. Forcing ns here keeps that conversion honest.
plot_df = plot_df.reset_index()
plot_df = plot_df.rename(columns={
    plot_df.columns[0]: 'date',
    'Open': 'open', 'High': 'high', 'Low': 'low',
    'Close': 'close', 'Volume': 'volume',
})
plot_df['date'] = plot_df['date'].dt.tz_localize(None).astype('datetime64[ns]')

# ---- colors ----
# A dark surface, so these are the dark steps -- not the light ones dimmed.
# EMA 50 is yellow rather than orange on purpose: an orange line sits right on
# top of red down-candles (indistinguishable even with full colour vision),
# and both share the price pane.
BG = '#161a1e'
UP, DOWN = '#26a69a', '#ef5350'
EMA_20, EMA_50 = '#3987e5', '#eda100'
BAND = '#787b86'
TEXT = '#d1d4dc'

# ======================================================================
# main chart: candles + overlays
# ======================================================================
chart = Chart(width=1400, height=900, title='RELIANCE.NS 1h', inner_height=0.5)
chart.layout(background_color=BG, text_color=TEXT, font_size=11)
chart.grid(color='#2a2e39')
chart.candle_style(
    up_color=UP, down_color=DOWN,
    border_up_color=UP, border_down_color=DOWN,
    wick_up_color=UP, wick_down_color=DOWN,
)
chart.crosshair(mode='normal', vert_color=BAND, horz_color=BAND)
# the TradingView-style legend: OHLC of the hovered bar plus each line's value
chart.legend(visible=True, ohlc=True, percent=True, lines=True,
             color=TEXT, font_size=11)
chart.watermark('RELIANCE.NS  1h', color='rgba(120,123,134,0.18)')

# create_line makes an empty series; .set() feeds it a frame carrying a 'date'
# column and one column named exactly like the line
ema20 = chart.create_line('EMA 20', color=EMA_20, width=2, price_line=False)
ema50 = chart.create_line('EMA 50', color=EMA_50, width=2, price_line=False)
bb_up = chart.create_line('BB upper', color=BAND, width=1,
                          style='dashed', price_line=False, price_label=False)
bb_low = chart.create_line('BB lower', color=BAND, width=1,
                           style='dashed', price_line=False, price_label=False)

# ======================================================================
# three synced panes underneath
# ======================================================================
# sync=True ties every subchart's time axis to the main chart, so zooming or
# panning one moves all four together.
# (Volume gets its own pane here to match plot1/plot2. TradingView's own habit
# is to overlay it on the price pane -- that's chart.volume_config() instead.)
vol_chart = chart.create_subchart(width=1, height=0.14, sync=True)
vol_chart.layout(background_color=BG, text_color=TEXT, font_size=11)
vol_chart.grid(color='#2a2e39')
vol_chart.legend(visible=True, color=TEXT, font_size=11, text='Volume')
volume = vol_chart.create_histogram('volume', price_line=False, price_label=False)

rsi_chart = chart.create_subchart(width=1, height=0.18, sync=True)
rsi_chart.layout(background_color=BG, text_color=TEXT, font_size=11)
rsi_chart.grid(color='#2a2e39')
rsi_chart.legend(visible=True, color=TEXT, font_size=11, text='RSI 14')
rsi = rsi_chart.create_line('RSI 14', color='#9085e9', width=2, price_line=False)
# reference levels drawn straight onto the pane
rsi_chart.horizontal_line(70, color=BAND, width=1, style='dashed', text='70')
rsi_chart.horizontal_line(30, color=BAND, width=1, style='dashed', text='30')

macd_chart = chart.create_subchart(width=1, height=0.18, sync=True)
macd_chart.layout(background_color=BG, text_color=TEXT, font_size=11)
macd_chart.grid(color='#2a2e39')
macd_chart.legend(visible=True, color=TEXT, font_size=11, text='MACD 12/26/9')
hist = macd_chart.create_histogram('Histogram', price_line=False, price_label=False)
macd_line = macd_chart.create_line('MACD', color=EMA_20, width=2, price_line=False)
signal_line = macd_chart.create_line('Signal', color=EMA_50, width=2, price_line=False)

# ======================================================================
# feed the data
# ======================================================================
chart.set(plot_df[['date', 'open', 'high', 'low', 'close']])

ema20.set(plot_df[['date', 'EMA 20']])
ema50.set(plot_df[['date', 'EMA 50']])
bb_up.set(plot_df[['date', 'BB upper']])
bb_low.set(plot_df[['date', 'BB lower']])

# a 'color' column lets a histogram paint each bar individually -- green when
# the candle closed up, red when it closed down
vol_df = plot_df[['date', 'volume']].copy()
vol_df['color'] = [UP if c >= o else DOWN
                   for c, o in zip(plot_df['close'], plot_df['open'])]
volume.set(vol_df)

rsi.set(plot_df[['date', 'RSI 14']])

hist_df = plot_df[['date', 'Histogram']].copy()
hist_df['color'] = [UP if v >= 0 else DOWN for v in plot_df['Histogram']]
hist.set(hist_df)
macd_line.set(plot_df[['date', 'MACD']])
signal_line.set(plot_df[['date', 'Signal']])

chart.show(block=True)
