import streamlit as st
import asyncio
from mcp_client import client_code

# --- Page Configuration ---
st.set_page_config(page_title="MarketPulse", layout="wide")
st.title("🤖 AI-Powered Financial Assistant with MCP Integration")

# --- Initialize Session State ---
# 'chat_history' stores the conversation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
# 'query_to_run' is a temporary state to hold the next query from any source
if "query_to_run" not in st.session_state:
    st.session_state.query_to_run = ""

# --- Helper function to set the next query ---
def submit_query(query_text: str):
    """Sets the query in session state to be processed in the next script run."""
    st.session_state.query_to_run = query_text

# --- Sidebar with Interactive Elements ---
with st.sidebar:
    st.header("🚀 Quick Actions")
    st.markdown("Use these shortcuts and templates to ask common questions.")

    st.subheader("Query Shortcuts")
    if st.button("What is the price of BTC?"):
        submit_query("What is the price of BTC?")

    if st.button("Latest stock market news"):
        submit_query("Latest stock market news")

    if st.button("What is the price of ETH?"):
        submit_query("What is the price of ETH?")

    st.divider()

    st.subheader("Query Templates")

    # Stock Price Template
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., GOOG, AAPL)", key="stock_symbol_input")
    if st.button("Get Stock Price"):
        if stock_symbol:
            submit_query(f"What is the current price of the stock with symbol {stock_symbol}?")
        else:
            st.warning("Please enter a stock symbol.")

    # Crypto Price Template
    crypto_symbol = st.text_input("Enter Crypto Symbol (e.g., SOL, XRP)", key="crypto_symbol_input")
    if st.button("Get Crypto Price"):
        if crypto_symbol:
            submit_query(f"What is the current price of the cryptocurrency {crypto_symbol}?")
        else:
            st.warning("Please enter a crypto symbol.")

# --- Main Chat Interface ---
# The chat input field at the bottom of the screen
if prompt := st.chat_input("Ask me anything about stocks, crypto, or news..."):
    submit_query(prompt)

# --- Core Logic: Process Query if one exists ---
# This block runs if a query was submitted either from the chat_input or a sidebar button
if st.session_state.query_to_run:
    # Retrieve the query and immediately clear the state to prevent re-running
    query = st.session_state.query_to_run
    st.session_state.query_to_run = ""

    # Add the user's query to the chat history
    st.session_state.chat_history.append(("user", query))

    # Display a spinner while waiting for the response
    with st.spinner("Thinking..."):
        try:
            # THIS IS THE UNCHANGED CORE LOGIC
            response = asyncio.run(client_code(query))
            st.session_state.chat_history.append(("bot", response))
        except Exception as e:
            st.session_state.chat_history.append(("bot", f"⚠️ Error: {e}"))
    
    # Rerun the script to immediately display the new messages
    st.rerun()

# --- Display Chat History ---
chat_container = st.container()
with chat_container:
    for role, msg in st.session_state.chat_history:
        if role == "user":
            with st.chat_message("user"):
                st.markdown(msg)
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg)