# Advanced Stock Analysis & Backtesting Tool 📈

A comprehensive, interactive web application for stock market analysis. Built with Python and Streamlit, this tool allows users to visualize historical stock data, apply technical indicators, and backtest a trading strategy to evaluate its historical performance.

---
## Features

* **Dynamic Data Fetching:** Fetches up-to-date historical stock data from the Yahoo Finance API using the `yfinance` library.
* **Interactive Visualizations:** Candlestick charts with zooming, panning, and hover-over details, powered by `Plotly`.
* **Customizable Technical Indicators:** Overlay popular indicators on the price chart, including:
    * 50-Day & 200-Day Simple Moving Averages (SMA)
    * Relative Strength Index (RSI)
    * Moving Average Convergence Divergence (MACD)
* **Advanced Backtesting Engine:** Implements a "Golden Cross" (SMA50/SMA200 crossover) trading strategy to quantitatively assess its performance against a simple "buy and hold" approach.
* **Intuitive UI:** A clean and responsive user interface built with Streamlit, featuring a sidebar for user inputs to keep the main view uncluttered.

---
## Technology Stack

* **Language:** Python
* **Web Framework:** Streamlit
* **Data Manipulation:** Pandas
* **Data Source:** yfinance (Yahoo Finance API)
* **Technical Analysis:** pandas-ta
* **Interactive Charting:** Plotly
---
## Getting Started
Follow these instructions to get a local copy of the project.

### Prerequisites
* Python 3.8 or higher
* pip package manager

### Installation
1.  **Clone the repository:**
2.  **Create and activate a virtual environment (recommended):**
3.  **Install the required dependencies:**
4.  **Run the Streamlit application:**

---
## Usage
1.  Enter a valid stock ticker symbol (e.g., `AAPL`, `AMZN`, `TSLA`) in the sidebar.
2.  Select the desired date range for analysis.
3.  Use the checkboxes to toggle technical indicators on the main price chart.
4.  Adjust the initial capital to see its effect on the backtesting simulation.
5.  Explore the charts and performance metrics to gain insights.
---
## Author
Created by **Astin**
* GitHub: `[@astin7](https://github.com/astin7)`
* LinkedIn: `https://www.linkedin.com/in/astin-huynh-3a4a24352/`
---
