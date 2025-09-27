import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from dashboard_utils import get_top_coins, get_price_trends, plot_price_trends, get_recent_alerts

st.set_page_config(page_title="Crypto Dashboard", layout="wide")
st.title("CRYPTO - DASH")

# --- Sidebar Filters ---
st.sidebar.header("Filters")
top_n = st.sidebar.slider("Top N Coins by Market Cap", min_value=5, max_value=50, value=20, step=5)
timeframe = st.sidebar.selectbox("Timeframe for Price Trend", ["24h", "7d", "30d"], index=1)

# --- Fetch top coins ---
coins_df = get_top_coins(top_n)
st.subheader(f"Top {top_n} Coins by Market Cap")
st.dataframe(coins_df)

# --- Price trends chart ---
time_map = {"24h": 1, "7d": 7, "30d": 30}
price_trends_df = get_price_trends(coins_df['coin_id'].tolist(), days=time_map[timeframe])
fig = plot_price_trends(price_trends_df, timeframe_label=f"Last {timeframe}")
if fig:
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No price data available for the selected timeframe.")

# --- Recent Alerts ---
st.subheader("🚨 Recent Price Alerts")
alerts_df = get_recent_alerts()
if not alerts_df.empty:
    st.dataframe(alerts_df)
else:
    st.info("No alerts detected yet.")
