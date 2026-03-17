import pandas as pd
from scoring import add_complexity_scores

tax_rate_file = "data/raw/tax_rate_data.csv"
time_file = "data/raw/time_data.csv"
payments_file = "data/raw/payments_data.csv"

year_col = "2019 [YR2019]"

tax_rate = pd.read_csv(tax_rate_file, encoding="latin1")
time_df = pd.read_csv(time_file, encoding="latin1")
payments = pd.read_csv(payments_file, encoding="latin1")

tax_rate = tax_rate[["Country Name", "Country Code", year_col]].copy()
time_df = time_df[["Country Name", "Country Code", year_col]].copy()
payments = payments[["Country Name", "Country Code", year_col]].copy()

tax_rate = tax_rate.rename(columns={year_col: "total_tax_rate"})
time_df = time_df.rename(columns={year_col: "time_hours"})
payments = payments.rename(columns={year_col: "payments_per_year"})

df = tax_rate.merge(time_df, on=["Country Name", "Country Code"], how="inner")
df = df.merge(payments, on=["Country Name", "Country Code"], how="inner")

for col in ["total_tax_rate", "time_hours", "payments_per_year"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["total_tax_rate", "time_hours", "payments_per_year"]).copy()

df = add_complexity_scores(df)

df = df.sort_values("complexity_score", ascending=False).reset_index(drop=True)

output_path = "data/processed/tax_complexity_dashboard_ready.csv"
df.to_csv(output_path, index=False)

print("Saved:", output_path)
print(df.head(10))