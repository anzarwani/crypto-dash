import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from utils.db_connector import supabase

# --- Fetch top N coins ---
def get_top_coins(n=20):
    response = supabase.table("coins").select("*").order("market_cap_rank").limit(n).execute()
    df = pd.DataFrame(response.data)
    return df

# --- Fetch price trends for selected coins ---
def get_price_trends(coin_ids, days=7):
    since = datetime.now() - timedelta(days=days)
    response = supabase.table("coin_prices").select("*").gte("timestamp", since.isoformat()).execute()
    df = pd.DataFrame(response.data)
    if df.empty:
        return df
    df = df[df['coin_id'].isin(coin_ids)]
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# --- Plot price trend chart ---
def plot_price_trends(df, timeframe_label=""):
    if df.empty:
        return None
    fig = px.line(df, x="timestamp", y="price", color="coin_id", 
                  title=f"Price Trends {timeframe_label}")
    return fig

# --- Fetch latest alerts ---
def get_recent_alerts(limit=20):
    response = supabase.table("alerts").select("*").order("timestamp", desc=True).limit(limit).execute()
    df = pd.DataFrame(response.data)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df
