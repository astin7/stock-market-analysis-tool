import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Page Configuration ---
st.set_page_config(
    page_title="Advanced Stock Analysis",
    page_icon="📈",
    layout="wide"
)

# --- Caching Data ---
@st.cache_data
def load_data(ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Loads historical stock data for a single ticker.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            return pd.DataFrame()
        
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        data.ta.sma(length=50, append=True)
        data.ta.sma(length=200, append=True)
        data.ta.rsi(append=True)
        data.ta.macd(append=True)
        
        data.rename(columns={
            "SMA_50": "SMA50",
            "SMA_200": "SMA200",
            "RSI_14": "RSI",
            "MACD_12_26_9": "MACD",
            "MACDh_12_26_9": "MACD_hist",
            "MACDs_12_26_9": "MACD_signal"
        }, inplace=True)
        
        return data.dropna()
    except Exception as e:
        st.error(f"Error loading data for {ticker}: {e}")
        return pd.DataFrame()

### NEW ### - Function to load data for multiple popular stocks
@st.cache_data
def load_popular_stocks_data(tickers: list, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Loads historical 'Close' price data for a list of tickers.
    """
    try:
        data = yf.download(tickers, start=start_date, end=end_date)['Close']
        return data
    except Exception as e:
        st.error(f"Error loading popular stock data: {e}")
        return pd.DataFrame()

# --- Backtesting Function (no changes here) ---
@st.cache_data
def run_backtest(data: pd.DataFrame, initial_capital: float = 10000.0) -> pd.DataFrame:
    """
    Performs a simple "Golden Cross" backtest (buy when SMA50 > SMA200).
    """
    data['Signal'] = 0
    data.loc[data['SMA50'] > data['SMA200'], 'Signal'] = 1
    data['Position'] = data['Signal'].diff()
    
    portfolio = pd.DataFrame(index=data.index)
    portfolio['Holdings'] = (data['Position'] * initial_capital / data['Close']).cumsum()
    portfolio['Cash'] = initial_capital - (data['Position'] * portfolio['Holdings']).cumsum()
    portfolio['Total'] = portfolio['Cash'] + portfolio['Holdings'] * data['Close']
    portfolio['Returns'] = portfolio['Total'].pct_change()
    
    return portfolio

# --- UI Layout ---

# Sidebar for user inputs (for single stock analysis)
st.sidebar.header("⚙️ Single Stock Analysis")
ticker = st.sidebar.text_input("Stock Ticker", "AAPL").upper()
start_date_single = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date_single = st.sidebar.date_input("End Date", datetime.now())

# Main content area
st.title("📈 Advanced Stock Analysis Dashboard")

### NEW ### - Top Market Movers Overview Section
st.subheader("📊 Top Market Movers Overview")
popular_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'JPM', 'V']

# Date range picker for the popular stocks chart
overview_range = st.date_input(
    "Select Date Range for Market Overview",
    (datetime.now() - timedelta(days=365), datetime.now()),
    key='overview_date_picker'
)

if len(overview_range) == 2:
    overview_start, overview_end = overview_range
    popular_df = load_popular_stocks_data(popular_tickers, overview_start, overview_end)

    if not popular_df.empty:
        # Normalize the data to see percentage growth
        normalized_df = (popular_df / popular_df.iloc[0]) * 100
        
        fig_popular = go.Figure()
        for ticker_symbol in normalized_df.columns:
            fig_popular.add_trace(go.Scatter(x=normalized_df.index, y=normalized_df[ticker_symbol], mode='lines', name=ticker_symbol))
            
        fig_popular.update_layout(
            title='Performance of Popular Stocks (Normalized to 100)',
            yaxis_title='Normalized Price',
            xaxis_title='Date',
            legend_title='Tickers'
        )
        st.plotly_chart(fig_popular, use_container_width=True)

# Visual separator
st.divider()

# --- Single Stock Analysis Section (moved down) ---
st.header(f"Deep Dive Analysis for: {ticker}")

# Load data for the single selected stock
df = load_data(ticker, start_date_single, end_date_single)

if df.empty:
    st.warning("No data found for the selected ticker and date range. Please try another ticker.")
else:
    # Display Key Metrics
    st.subheader("Key Metrics")
    latest_price = df['Close'].iloc[-1]
    prev_price = df['Close'].iloc[-2]
    price_change = latest_price - prev_price
    pct_change = (price_change / prev_price) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Last Close Price", f"${latest_price:,.2f}", f"{price_change:,.2f} ({pct_change:.2f}%)")
    col2.metric("52-Week High", f"${df['High'].max():,.2f}")
    col3.metric("52-Week Low", f"${df['Low'].min():,.2f}")

    # --- Interactive Price Chart ---
    st.subheader("Price Chart with Technical Indicators")
    fig_price = go.Figure()
    
    fig_price.add_trace(go.Candlestick(x=df.index,
                                       open=df['Open'],
                                       high=df['High'],
                                       low=df['Low'],
                                       close=df['Close'],
                                       name='Price'))
    
    show_sma50 = st.checkbox("Show 50-Day SMA", value=True)
    show_sma200 = st.checkbox("Show 200-Day SMA", value=True)
    if show_sma50:
        fig_price.add_trace(go.Scatter(x=df.index, y=df['SMA50'], mode='lines', name='50-Day SMA', line=dict(color='orange', width=1.5)))
    if show_sma200:
        fig_price.add_trace(go.Scatter(x=df.index, y=df['SMA200'], mode='lines', name='200-Day SMA', line=dict(color='purple', width=1.5)))
    
    fig_price.update_layout(
        title=f'{ticker} Price History',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_price, use_container_width=True)
    
    # --- Technical Indicator Subplots ---
    st.subheader("Technical Indicators")
    
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI', line=dict(color='green')))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="blue", annotation_text="Oversold")
    fig_rsi.update_layout(title='Relative Strength Index (RSI)', yaxis_title='RSI')
    st.plotly_chart(fig_rsi, use_container_width=True)
    
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')))
    fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'], name='Signal Line', line=dict(color='orange')))
    fig_macd.add_bar(x=df.index, y=df['MACD_hist'], name='Histogram', marker_color=df['MACD_hist'].apply(lambda x: 'green' if x >= 0 else 'red'))
    fig_macd.update_layout(title='MACD', yaxis_title='Value')
    st.plotly_chart(fig_macd, use_container_width=True)

    # --- Backtesting Section ---
    st.subheader("✨ Golden Cross Strategy Backtest")
    st.markdown("""
    This backtest simulates a simple trading strategy:
    - **Buy Signal:** When the 50-day Simple Moving Average (SMA50) crosses **above** the 200-day SMA.
    - **Position:** The strategy holds the stock as long as the SMA50 is above the SMA200.
    """)
    
    initial_capital = st.number_input("Initial Capital for Backtest", 10000.0, step=1000.0)
    
    portfolio = run_backtest(df, initial_capital)
    
    final_value = portfolio['Total'].iloc[-1]
    total_return = (final_value - initial_capital) / initial_capital * 100
    buy_hold_return = (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100
    
    col1_bt, col2_bt, col3_bt = st.columns(3)
    col1_bt.metric("Final Portfolio Value", f"${final_value:,.2f}")
    col2_bt.metric("Strategy Total Return", f"{total_return:.2f}%")
    col3_bt.metric("Buy & Hold Return", f"{buy_hold_return:.2f}%")
    
    fig_portfolio = go.Figure()
    fig_portfolio.add_trace(go.Scatter(x=portfolio.index, y=portfolio['Total'], mode='lines', name='Strategy Performance'))
    fig_portfolio.update_layout(title='Portfolio Value Over Time', yaxis_title='Portfolio Value (USD)')
    st.plotly_chart(fig_portfolio, use_container_width=True)

    # --- Raw Data Display ---
    with st.expander("View Raw Data"):
        st.dataframe(df.style.format("{:.2f}"))