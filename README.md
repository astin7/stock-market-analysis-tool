# Stock Analysis Dashboard 📈
A comprehensive, interactive web application for stock market analysis built with Python and Streamlit. This dashboard provides an overview of a high-level market and allows users to complete a deep-dive analysis on individual stocks, including technical indicators and strategy backtesting.
---
## Features
* **Market Overview Dashboard:** Instantly compare the normalized performance of top market-leading stocks (e.g., AAPL, MSFT, GOOGL) over a customizable time frame to gauge overall market trends.
* **Deep Dive Analysis:** Focus on any single stock by entering its ticker symbol for detailed analysis.
* **Interactive Visualizations:** Candlestick charts with zooming, panning, and hover-over details, powered by `Plotly`.
* **Customizable Technical Indicators:** Overlay popular indicators on the price chart, including:
    * 50-Day & 200-Day Simple Moving Averages (SMA)
    * Relative Strength Index (RSI)
    * Moving Average Convergence Divergence (MACD)
* **Advanced Backtesting Engine:** Implements a "Golden Cross" (SMA50/SMA200 crossover) trading strategy to quantitatively assess its performance against a simple "buy and hold" approach.
* **Intuitive UI:** A clean and responsive user interface built with Streamlit, featuring a top-level overview and a sidebar for detailed single-stock analysis.
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
Follow these instructions to get a local copy of the project up and running.

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
1.  Use the date range picker at the top of the page to adjust the time frame for the **Market Overview** chart.
2.  For a detailed analysis, enter a valid stock ticker symbol (e.g., `AAPL`, `MSFT`, `TSLA`) in the **sidebar** on the left.
3.  Use the checkboxes in the main area to toggle technical indicators on the single-stock price chart.
4.  Adjust the initial capital to see its effect on the backtesting simulation.
5.  Explore the charts and performance metrics to gain insights.
---
## Author
Created by **Astin**
* GitHub: `[@astin7](https://github.com/astin7)`
* LinkedIn: `https://www.linkedin.com/in/astin-huynh-3a4a24352/`
---
## License
This project is licensed under the MIT License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
