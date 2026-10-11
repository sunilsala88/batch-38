# Same chart as plot1.py, drawn with plotly instead of mplfinance.
# The difference that matters: this one is interactive -- hover for values,
# drag to zoom, double-click to reset -- and it opens in a browser.
import yfinance as yf
import pandas_ta_classic as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = yf.download("RELIANCE.NS", period="730d", interval="1h", multi_level_index=False)

# ---- indicators (computed on the FULL history, sliced afterwards) ----
df['ema_20'] = ta.ema(df['Close'], length=20)
df['ema_50'] = ta.ema(df['Close'], length=50)

bb = ta.bbands(df['Close'], length=20, std=2)
df['bb_low'] = bb['BBL_20_2.0']
df['bb_up'] = bb['BBU_20_2.0']

df['rsi'] = ta.rsi(df['Close'], length=14)

macd = ta.macd(df['Close'], fast=12, slow=26, signal=9)
df['macd'] = macd['MACD_12_26_9']
df['macd_signal'] = macd['MACDs_12_26_9']
df['macd_hist'] = macd['MACDh_12_26_9']

BARS = 150
plot_df = df.tail(BARS)

UP, DOWN = '#008300', '#e34948'
# EMA 50 is amber rather than orange deliberately: an orange line lands on top
# of the red down-candles it shares the panel with, and the two are hard to
# tell apart even with full colour vision.
EMA_20, EMA_50 = '#2a78d6', '#c98500'
BAND = '#9a9890'
GRID = '#e8e7e1'

# ======================================================================
# four stacked panels sharing one x-axis
# ======================================================================
# shared_xaxes means zooming the price panel zooms all four together.
# Each oscillator gets its own row instead of a second y-axis on the price
# chart -- two scales on one plot can be stretched to imply any relationship.
fig = make_subplots(
    rows=4, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    row_heights=[0.55, 0.12, 0.16, 0.17],
    subplot_titles=('', '', '', ''),
)

# ---- row 1: candles + overlays ----
fig.add_trace(go.Candlestick(
    x=plot_df.index,
    open=plot_df['Open'], high=plot_df['High'],
    low=plot_df['Low'], close=plot_df['Close'],
    increasing_line_color=UP, increasing_fillcolor=UP,
    decreasing_line_color=DOWN, decreasing_fillcolor=DOWN,
    line_width=1,
    name='Price',
    showlegend=False,   # the candles are self-evident; keep the legend for lines
), row=1, col=1)

# upper band first, then the lower one with fill='tonexty' so plotly shades
# the channel between the two traces
fig.add_trace(go.Scatter(
    x=plot_df.index, y=plot_df['bb_up'], name='Bollinger 20/2',
    line=dict(color=BAND, width=1, dash='dash'),
    legendgroup='bb', hoverinfo='skip',
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=plot_df.index, y=plot_df['bb_low'], name='Bollinger 20/2',
    line=dict(color=BAND, width=1, dash='dash'),
    fill='tonexty', fillcolor='rgba(154,152,144,0.10)',
    legendgroup='bb', showlegend=False, hoverinfo='skip',
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=plot_df.index, y=plot_df['ema_20'], name='EMA 20',
    line=dict(color=EMA_20, width=1.6),
), row=1, col=1)
fig.add_trace(go.Scatter(
    x=plot_df.index, y=plot_df['ema_50'], name='EMA 50',
    line=dict(color=EMA_50, width=1.6),
), row=1, col=1)

# ---- row 2: volume ----
fig.add_trace(go.Bar(
    x=plot_df.index, y=plot_df['Volume'], name='Volume',
    marker_color=[UP if c >= o else DOWN
                  for c, o in zip(plot_df['Close'], plot_df['Open'])],
    marker_line_width=0, opacity=0.65, showlegend=False,
), row=2, col=1)

# ---- row 3: RSI ----
fig.add_trace(go.Scatter(
    x=plot_df.index, y=plot_df['rsi'], name='RSI 14',
    line=dict(color='#4a3aa7', width=1.6), showlegend=False,
), row=3, col=1)
# add_hline with a row= draws the reference line on that panel only
for level in (30, 70):
    fig.add_hline(y=level, line=dict(color=BAND, width=1, dash='dot'),
                  row=3, col=1)

# ---- row 4: MACD ----
fig.add_trace(go.Bar(
    x=plot_df.index, y=plot_df['macd_hist'], name='MACD hist',
    marker_color=[UP if v >= 0 else DOWN for v in plot_df['macd_hist']],
    marker_line_width=0, opacity=0.5, showlegend=False,
), row=4, col=1)
fig.add_trace(go.Scatter(
    x=plot_df.index, y=plot_df['macd'], name='MACD',
    line=dict(color=EMA_20, width=1.6), showlegend=False,
), row=4, col=1)
fig.add_trace(go.Scatter(
    x=plot_df.index, y=plot_df['macd_signal'], name='Signal',
    line=dict(color=EMA_50, width=1.6), showlegend=False,
), row=4, col=1)

# ======================================================================
# layout
# ======================================================================
fig.update_layout(
    title=dict(text=f'RELIANCE.NS &nbsp;1h &nbsp;(last {BARS} bars)',
               x=0.01, font=dict(size=18, color='#0b0b0b')),
    height=900, width=1400,
    paper_bgcolor='#fcfcfb', plot_bgcolor='#fcfcfb',
    font=dict(color='#52514e', size=11),
    # one shared tooltip listing every series at the hovered bar, instead of
    # nine separate ones you have to hunt for
    hovermode='x unified',
    hoverlabel=dict(bgcolor='#ffffff', font_size=11),
    legend=dict(orientation='h', yanchor='bottom', y=1.01,
                xanchor='right', x=1, bgcolor='rgba(0,0,0,0)'),
    margin=dict(l=60, r=30, t=80, b=40),
    bargap=0.15,
)

# the candlestick rangeslider is on by default and eats a lot of height --
# with four linked panels the box-zoom is the better tool
fig.update_xaxes(rangeslider_visible=False)

# yfinance hands back only market hours, but the x-axis is a real timeline, so
# plotly leaves a flat gap for every night and weekend. rangebreaks cut those
# out: NSE trades 09:15-15:30 IST, Mon-Fri.
fig.update_xaxes(rangebreaks=[
    dict(bounds=['sat', 'mon']),
    dict(bounds=[15.5, 9.25], pattern='hour'),
])

fig.update_xaxes(showgrid=True, gridcolor=GRID, showline=True, linecolor=GRID)
fig.update_yaxes(showgrid=True, gridcolor=GRID, showline=True, linecolor=GRID,
                 zeroline=False)

fig.update_yaxes(title_text='Price', row=1, col=1)
fig.update_yaxes(title_text='Volume', row=2, col=1)
# RSI is bounded 0-100, so pin the scale -- otherwise 30 and 70 drift around
fig.update_yaxes(title_text='RSI 14', range=[0, 100], dtick=25, row=3, col=1)
fig.update_yaxes(title_text='MACD', row=4, col=1)

fig.write_html('reliance_candles.html')
fig.show()
