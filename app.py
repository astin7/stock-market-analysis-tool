import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Advanced Stock Analysis",
    page_icon="📈",
    layout="wide"
)

# Caching Data 
# Use Streamlit's caching to avoid re-downloading data on every interaction.
@st.cache_data
def load_data(ticker: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """
    Loads historical stock data from Yahoo Finance, calculates technical indicators,
    and returns a pandas DataFrame.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            return pd.DataFrame() # Return empty DataFrame if no data
        
        # Flatten the column headers if they are a MultiIndex
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        # Calculate technical indicators using pandas-ta
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
        
        return data.dropna() # Drop rows with NaN values
    except Exception as e:
        st.error(f"Error loading data for {ticker}: {e}")
        return pd.DataFrame()

# Backtesting Function
@st.cache_data
def run_backtest(data: pd.DataFrame, initial_capital: float = 10000.0) -> pd.DataFrame:
    """
    Performs a simple "Golden Cross" backtest (buy when SMA50 > SMA200).
    """
    data['Signal'] = 0
    # Generate signal: 1 for Buy, -1 for Sell
    data.loc[data['SMA50'] > data['SMA200'], 'Signal'] = 1
    
    # Calculate daily position changes (buy/sell triggers)
    data['Position'] = data['Signal'].diff()
    
    portfolio = pd.DataFrame(index=data.index)
    portfolio['Holdings'] = (data['Position'] * initial_capital / data['Close']).cumsum()
    portfolio['Cash'] = initial_capital - (data['Position'] * portfolio['Holdings']).cumsum()
    portfolio['Total'] = portfolio['Cash'] + portfolio['Holdings'] * data['Close']
    portfolio['Returns'] = portfolio['Total'].pct_change()
    
    return portfolio

# UI Layout
# Sidebar for user inputs
st.sidebar.header("User Inputs ⚙️")
ticker = st.sidebar.text_input("Stock Ticker", "AAPL").upper()
start_date = st.sidebar.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.now())

# Main content area
st.title(f"Advanced Stock Analysis for {ticker} 📈")

# Load data
df = load_data(ticker, start_date, end_date)

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

    # Interactive Price Chart
    st.subheader("Price Chart with Technical Indicators")
    fig_price = go.Figure()
    
    # Add Closing Price trace
    fig_price.add_trace(go.Candlestick(x=df.index,
                                       open=df['Open'],
                                       high=df['High'],
                                       low=df['Low'],
                                       close=df['Close'],
                                       name='Price'))
    
    # Add selectable Moving Averages
    show_sma50 = st.checkbox("Show 50-Day SMA", value=True)
    show_sma200 = st.checkbox("Show 200-Day SMA", value=True)
    if show_sma50:
        fig_price.add_trace(go.Scatter(x=df.index, y=df['SMA50'], mode='lines', name='50-Day SMA', line=dict(color='orange', width=1.5)))
    if show_sma200:
        fig_price.add_trace(go.Scatter(x=df.index, y=df['SMA200'], mode='lines', name='200-Day SMA', line=dict(color='purple', width=1.5)))
    
    fig_price.update_layout(
        title=f'{ticker} Price History',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False, # Hide the range slider for a cleaner look
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_price, use_container_width=True)
    
    # Technical Indicator Subplots
    st.subheader("Technical Indicators")
    
    # RSI Chart
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name='RSI', line=dict(color='green')))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="blue", annotation_text="Oversold")
    fig_rsi.update_layout(title='Relative Strength Index (RSI)', yaxis_title='RSI')
    st.plotly_chart(fig_rsi, use_container_width=True)
    
    # MACD Chart
    fig_macd = go.Figure()
    fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')))
    fig_macd.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'], name='Signal Line', line=dict(color='orange')))
    fig_macd.add_bar(x=df.index, y=df['MACD_hist'], name='Histogram', marker_color=df['MACD_hist'].apply(lambda x: 'green' if x >= 0 else 'red'))
    fig_macd.update_layout(title='MACD', yaxis_title='Value')
    st.plotly_chart(fig_macd, use_container_width=True)

    # Backtesting Section
    st.subheader("Golden Cross Strategy Backtest")
    st.markdown("""
    This backtest simulates a simple trading strategy:
    - **Buy Signal:** When the 50-day Simple Moving Average (SMA50) crosses **above** the 200-day SMA (a "Golden Cross").
    - **Sell Signal:** Not explicitly defined, the strategy simply holds the position while SMA50 is above SMA200.
    """)
    
    initial_capital = st.number_input("Initial Capital for Backtest", 10000.0, step=1000.0)
    
    portfolio = run_backtest(df, initial_capital)
    
    # Display Backtest Performance
    final_value = portfolio['Total'].iloc[-1]
    total_return = (final_value - initial_capital) / initial_capital * 100
    
    buy_hold_return = (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100
    
    col1_bt, col2_bt, col3_bt = st.columns(3)
    col1_bt.metric("Final Portfolio Value", f"${final_value:,.2f}")
    col2_bt.metric("Strategy Total Return", f"{total_return:.2f}%")
    col3_bt.metric("Buy & Hold Return", f"{buy_hold_return:.2f}%")
    
    # Plot Portfolio Value
    fig_portfolio = go.Figure()
    fig_portfolio.add_trace(go.Scatter(x=portfolio.index, y=portfolio['Total'], mode='lines', name='Strategy Performance'))
    fig_portfolio.update_layout(title='Portfolio Value Over Time', yaxis_title='Portfolio Value (USD)')
    st.plotly_chart(fig_portfolio, use_container_width=True)

    # Raw Data Display
    with st.expander("View Raw Data"):
        st.dataframe(df.style.format("{:.2f}"))