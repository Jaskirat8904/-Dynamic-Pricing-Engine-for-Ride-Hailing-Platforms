def compute_kpis(df):
    if df is None or df.empty:
        return {}

    return {
        "windows": len(df),
        "avg_surge": round(df["surge_multiplier"].mean(), 2),
        "max_surge": round(df["surge_multiplier"].max(), 2),
        "avg_demand": round(df["demand"].mean(), 2),
        "avg_supply": round(df["supply"].mean(), 2),
    }
