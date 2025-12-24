import streamlit as st
import pandas as pd
from backend import BasicBot

st.set_page_config(page_title="Crypto Bot Dashboard", layout="wide")

# --- 1. Persistent State ---
if "bot" not in st.session_state:
    st.session_state.bot = None
if "history" not in st.session_state:
    st.session_state.history = []

# --- 2. Sidebar Credentials ---
with st.sidebar:
    st.header("🔑 API Settings")
    key = st.text_input("API Key", type="default")
    secret = st.text_input("API Secret", type="password")
    if st.button("Connect Bot"):
        try:
            st.session_state.bot = BasicBot(key, secret)
            st.success("Connected to Testnet!")
        except Exception as e:
            st.error(f"Failed: {e}")

# --- 3. Dashboard Body ---
if st.session_state.bot:
    st.title("Binance Trading Bot")
    st.divider()
    bot = st.session_state.bot
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Market Data")

        symbols = bot.get_symbols()
        symbol = st.selectbox("Trading Pair", symbols[:10])

        price = bot.get_price(symbol)
        st.metric(label=f"Current {symbol} Price", value=f"${price:,.4f}")
        
        balance = bot.get_balance()
        st.metric(label="USDT Balance", value=f"${float(balance):,.4f}")

    with col2:
        st.subheader("🛒 Place Order")
        with st.form("trade_form"):
            side = st.radio("Side", ["BUY", "SELL"], horizontal=True)
            order_type = st.selectbox("Order Type", ["MARKET", "LIMIT"])
            qty = st.number_input("Quantity", min_value=0.001, step=0.001)
            limit_price = st.number_input("Limit Price (if applicable)", value=price)
            
            if st.form_submit_button("Execute Trade"):
                response = bot.place_order(symbol, side, order_type, qty, limit_price)

                if "error" in response:
                    st.error(response["error"])
                elif "validation_error" in response:
                    st.error("Validation Failed:")
                    for msg in response["validation_error"]:
                        st.write(f"- {msg}")
                else:
                    st.success(f"Order Executed! - OrderID: {response['orderId']}")
                    st.session_state.history.append(response)

    # --- 4. Order History ---
    st.divider()
    st.subheader("📜Order Details")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df[['orderId', 'symbol', 'side', 'type', 'status', 'avgPrice', 'price']], width='stretch', )
else:
    st.title("Binance Trading Bot")
    st.divider()
    st.info("Enter your API keys in the sidebar to start.")