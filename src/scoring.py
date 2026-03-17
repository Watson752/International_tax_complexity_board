import pandas as pd

def minmax(series: pd.Series) -> pd.Series:
    return 100 * (series - series.min()) / (series.max() - series.min())

def assign_band(score: float) -> str:
    if score >= 75:
        return "Very High"
    elif score >= 50:
        return "High"
    elif score >= 25:
        return "Medium"
    return "Low"

def add_complexity_scores(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["tax_rate_score"] = minmax(df["total_tax_rate"])
    df["time_score"] = minmax(df["time_hours"])
    df["payments_score"] = minmax(df["payments_per_year"])

    df["complexity_score"] = (
        0.30 * df["tax_rate_score"] +
        0.40 * df["time_score"] +
        0.30 * df["payments_score"]
    ).round(1)

    df["complexity_band"] = df["complexity_score"].apply(assign_band)

    return df