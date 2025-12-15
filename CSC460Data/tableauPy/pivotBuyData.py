import pandas as pd

# Read BuyData CSV, skip unnamed index if present
buy_df = pd.read_csv("AllResults/BuyData.csv", index_col=0)

# ID columns to keep
id_cols = ["RegionID", "SizeRank", "RegionName", "RegionType", "StateName"]

# Melt date columns into long format
long_buy_df = buy_df.melt(
    id_vars=id_cols,
    var_name="Date",
    value_name="PriceValue"
)

# Convert Date to datetime
long_buy_df["Date"] = pd.to_datetime(long_buy_df["Date"], errors='coerce')

# Drop rows where date conversion failed
long_buy_df = long_buy_df.dropna(subset=["Date"])

# Optional: save to CSV
long_buy_df.to_csv("tableauData/BuyData_long.csv", index=False)

print(long_buy_df.head())
