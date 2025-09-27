import requests
import json
import pandas as pd
from datetime import datetime
from utils.helpers import handle_api_errors

# Load config
with open("config.json") as f:
    config = json.load(f)

COINGECKO_API = config['coingecko_api_url']

def fetch_top_coins(vs_currency="usd", per_page=50, page=1):
    """
    Fetch top coins by market cap from CoinGecko
    Returns a DataFrame with coin_id, name, symbol, market_cap_rank, price, volume, market_cap, timestamp
    """
    url = f"{COINGECKO_API}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "price_change_percentage": "1h,24h,7d"
    }

    response = handle_api_errors(requests.get, url, params=params)
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data)
    if df.empty:
        return df

    df = df[[
        "id", "name", "symbol", "market_cap_rank",
        "current_price", "total_volume", "market_cap"
    ]]

    # Rename columns for ETL consistency
    df = df.rename(columns={
        "id": "coin_id",
        "current_price": "price",
        "total_volume": "volume"
    })

    # Add timestamp
    df["timestamp"] = datetime.now()

    return df

if __name__ == "__main__":
    df = fetch_top_coins()
    #print(df.head())
