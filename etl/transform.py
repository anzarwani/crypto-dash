import pandas as pd
from datetime import datetime

def calculate_percent_change(df, period_cols=["price"]):
    """
    Calculate percent change for given columns compared to previous row.
    Assumes df is sorted by coin_id and timestamp ascending.
    """
    df = df.sort_values(["coin_id", "timestamp"])
    
    for col in period_cols:
        df[f"{col}_pct_change"] = df.groupby("coin_id")[col].pct_change() * 100
    return df

def detect_anomalies(df, price_change_threshold=5):
    """
    Detects anomalies based on sudden price changes.
    Returns a DataFrame with anomalies only.
    """
    anomalies = df[df["price_pct_change"].abs() >= price_change_threshold].copy()
    anomalies["alert_type"] = "PRICE_JUMP"
    anomalies["alert_timestamp"] = datetime.now()
    return anomalies

def transform(df):
    """
    Main transform function
    - Calculates % change for price
    - Detects anomalies
    Returns:
        df_transformed: cleaned and enriched DataFrame
        df_anomalies: DataFrame of anomalies for alerts
    """
    if df.empty:
        return df, pd.DataFrame()

    # Calculate price % change
    df_transformed = calculate_percent_change(df, ["price"])

    # Detect anomalies
    df_anomalies = detect_anomalies(df_transformed)

    return df_transformed, df_anomalies

if __name__ == "__main__":
    # Quick test with extract.py
    from etl.extract import fetch_top_coins

    df = fetch_top_coins()
    df_transformed, df_anomalies = transform(df)

    # print("Transformed Data:")
    # print(df_transformed.head())

    # print("\nAnomalies Detected:")
    # print(df_anomalies.head())
