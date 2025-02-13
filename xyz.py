import streamlit as st
from langchain.embeddings.google_palm import GooglePalmEmbeddings
#from yfinance import Ticker
import pandas as pd
import plotly.graph_objects as go

# Initialize Google Palm embeddings using Gemini
api_key = "AIzaSyCCw-l2HgxXQMMvDdN_CEMB2SqYwLMbuP0"
embeddings = GooglePalmEmbeddings(model="model/embedding-001", google_api_key=api_key)

# Load stock data from CSV
@st.cache_data
def load_stock_data(file_path):
    try:
        data = pd.read_csv(file_path)
        if data.empty:
            st.warning("Loaded stock data is empty.")
        return data
    except Exception as e:
        st.error(f"Error loading stock data: {e}")
        return pd.DataFrame()

# Load the stock data
stock_data = load_stock_data("SamplePortfolio.csv")

# Initialize Streamlit for UI
st.title("Custom Stock Market Assistant")


import streamlit as st

# Add a sidebar with a selectbox to select the page
page = st.sidebar.selectbox("Choose a page", ["Home", "IPO Data", "About"])

# Based on the page selected, show content
if page == "Home":
    def tradingview_chart_html(symbol, width="100%", height="500"):
        return f"""
    <div class="tradingview-widget-container">
      <div id="tradingview_{symbol}"></div>
      <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
      <script type="text/javascript">
      new TradingView.widget(
        {{
          "width": "{width}",
          "height": "{height}",
          "symbol": "{symbol}",
          "interval": "D",  // Default to 5-minute chart
          "timezone": "Etc/UTC",
          "theme": "{st.sidebar.radio("Select Theme of Chart", ["Light", "Dark"])}",
          "style": "1",
          "locale": "en",
          "toolbar_bg": "#f1f3f6",
          "overrides": {{
            "study_Overlay@tv-basicstudies": {{
              "inputs": {{
                "length": 50
              }},
              "name": "EMA 50"
            }},
            "study_Overlay@tv-basicstudies:1": {{
              "inputs": {{
                "length": 200
              }},
              "name": "EMA 200"
            }}
          }},
          "studies": [
            "Moving Average Exponential@tv-basicstudies",  // Default EMA
            "RSI@tv-basicstudies",                        // RSI
            "MACD@tv-basicstudies",                       // MACD
            "Bollinger Bands@tv-basicstudies"             // Bollinger Bands
          ],
          "enable_publishing": false,
          "hide_top_toolbar": true,
          "save_image": false,
          "container_id": "tradingview_{symbol}"
        }}
      );
      </script>
    </div>
    """


# Fetch stock data
def fetch_stock_data(symbol, period):
    try:
        ticker = Ticker(symbol)
        history = ticker.history(period=period)  # Fetch stock history
        return history
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return None




# Stock search feature
st.header("Stock Search")

# Ensure stock_data is valid before proceeding
if not stock_data.empty and 'Company Name' in stock_data.columns:
    #st.write("Loaded Stock Data:")
    #st.dataframe(stock_data.head())

    selected_stock = st.selectbox(
        "Select a stock name:",
        [""] + stock_data['Company Name'].tolist(),
        format_func=lambda x: "Select a stock" if x == "" else x
    )

    if selected_stock and selected_stock != "":
        matching_symbols = stock_data.loc[stock_data['Company Name'] == selected_stock, 'Symbol'].values
        if len(matching_symbols) > 0:
            selected_symbol = matching_symbols[0]
        else:
            selected_symbol = None
            st.warning("No matching symbol found for the selected stock.")
    else:
        selected_symbol = None
        st.info("Please select a stock.")
else:
    st.warning("Stock data is empty or 'Company Name' column is missing.")
    selected_stock = None
    selected_symbol = None

# Display the selected stock symbol in a text input box
stock_input = st.text_input("Stock Symbol:", value=selected_symbol if selected_symbol else "", disabled=True)


# Validate and update stock input if necessary
#if stock_input and not (stock_input.endswith(".NS") or stock_input.endswith(".BO")):
#    stock_input += ".NS"

# Time period selection
time_period="1y"


# Function to generate TradingView chart HTML with indicators, including EMA 50 and EMA 200
# Function to generate TradingView chart HTML with EMA and other indicators










# Input for Stock Symbol

if stock_input and page == "Home" :
    # Render TradingView Chart
    chart_html = tradingview_chart_html(stock_input)
    st.components.v1.html(chart_html, height=500)
    



# Footer
st.markdown("""
    <style>
        .footer {
            text-align: center;
            font-size: 14px;
            color: #888888;
            margin-top: 20px;
        }
        
    </style>
    <div class="footer">
        🛠️ Developed by RK | 🌟 Built with LangChain 🤖, 🌌 Gemini, and ⚡ Streamlit | 📊 Powered by CSV Data 📂✨
    </div>
""", unsafe_allow_html=True)