import pandas as pd

# Load your actual CSV (update name if needed)
df = pd.read_csv("forcast_housePrice_data (1).csv")

# Convert Year column to datetime
df["Year"] = pd.to_datetime(df["Year"])

# Extract year number only (e.g., 2015, 2016…)
df["YearNum"] = df["Year"].dt.year

# Convert prices to numeric
df["medianHousePrice"] = pd.to_numeric(df["medianHousePrice"], errors="coerce")

# Drop missing rows
df = df.dropna(subset=["medianHousePrice"])

# --- GROUP TO YEARLY AVERAGE ---
yearly = (
    df.groupby(["County", "YearNum"])["medianHousePrice"]
      .mean()
      .reset_index()
      .sort_values(["County", "YearNum"])
)

# Save cleaned output
yearly.to_csv("house_price_yearly.csv", index=False)

print("\n✅ CLEANED YEARLY HOUSE PRICE DATA")
print(yearly.head(20))
print("\n📁 Saved → house_price_yearly.csv")
