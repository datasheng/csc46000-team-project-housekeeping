import pandas as pd

# Read CSV, using first column as index if it's an unnamed index
df = pd.read_csv("AllResults/RentData.csv", index_col=0)

id_cols = [
    "RegionID", "SizeRank", "RegionName", "RegionType",
    "StateName", "State", "Metro", "StateCodeFIPS", "MunicipalCodeFIPS"
]

# Melt to long format
long_df = df.melt(
    id_vars=id_cols,
    var_name="Date",
    value_name="MedianValue"
)

# Drop any rows where Date is not a valid string (if needed)
long_df = long_df[long_df["Date"].notna()]

# Convert Date to datetime, adjust format if your CSV has MM/DD/YYYY or YYYY-MM-DD
long_df["Date"] = pd.to_datetime(long_df["Date"], errors='coerce')

# Optional: drop rows where conversion failed
long_df = long_df.dropna(subset=["Date"])

print(long_df.head())
long_df.to_csv("tableauData/pivotBuyData.csv", index=False)
