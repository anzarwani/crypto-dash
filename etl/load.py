from utils.db_connector import supabase
import pandas as pd

def upsert_coins(df):
    """
    Upsert coin metadata into `coins` table
    """
    if df.empty:
        return

    coins_df = df[['coin_id', 'name', 'symbol', 'market_cap_rank']].drop_duplicates(subset=['coin_id'])
    for _, row in coins_df.iterrows():
        supabase.table("coins").upsert({
            "coin_id": row['coin_id'],
            "name": row['name'],
            "symbol": row['symbol'],
            "market_cap_rank": row['market_cap_rank']
        }, on_conflict="coin_id").execute()


def insert_coin_prices(df):
    """
    Insert new price snapshots into `coin_prices` table
    """
    if df.empty:
        return

    prices_df = df[['coin_id', 'timestamp', 'price', 'volume', 'market_cap']].copy()
    # Convert timestamp to ISO format string
    prices_df['timestamp'] = prices_df['timestamp'].apply(lambda x: x.isoformat())

    data_to_insert = prices_df.to_dict(orient="records")
    supabase.table("coin_prices").insert(data_to_insert).execute()


def insert_alerts(df):
    """
    Insert new anomalies into `alerts` table
    """
    if df.empty:
        return

    alerts_df = df[['coin_id', 'alert_timestamp', 'price_pct_change', 'alert_type']].copy()
    # Rename columns
    alerts_df = alerts_df.rename(columns={'alert_timestamp': 'timestamp', 'price_pct_change': 'price_change_pct'})
    # Convert timestamp to ISO
    alerts_df['timestamp'] = alerts_df['timestamp'].apply(lambda x: x.isoformat())

    data_to_insert = alerts_df.to_dict(orient="records")
    supabase.table("alerts").insert(data_to_insert).execute()


def load(df_transformed, df_anomalies):
    """
    Main load function
    """
    upsert_coins(df_transformed)
    insert_coin_prices(df_transformed)
    insert_alerts(df_anomalies)


if __name__ == "__main__":
    # Quick test with extract + transform
    from etl.extract import fetch_top_coins
    from etl.transform import transform

    df = fetch_top_coins()
    df_transformed, df_anomalies = transform(df)

    load(df_transformed, df_anomalies)
    # print("Load complete.")
