import requests
import pandas as pd
from prophet import Prophet

# -------------------------------------------
# CONFIG
# -------------------------------------------
API_KEY = "6b31c2d41f669896f9f32d1b16d1a2b38950be89"
FORECAST_YEARS = 10   # Forecast 10 future years
START_YEAR = 2015
END_YEAR = 2023

# -------------------------------------------
# STEP 1: Download Historical Data
# -------------------------------------------

print("📡 Downloading historical rent data from Census API...")

all_rows = []

for year in range(START_YEAR, END_YEAR + 1):
    url = (
        f"https://api.census.gov/data/{year}/acs/acs5"
        f"?get=NAME,B25058_001E"
        f"&for=county:*"
        f"&in=state:36"
        f"&key={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    headers = data[0]
    rows = data[1:]

    for row in rows:
        county_name = row[0].replace(" County, New York", "")
        median_rent = row[1]

        if median_rent is None or median_rent == "":
            continue

        all_rows.append({
            "County": county_name,
            "Year": year,
            "MedianRent": float(median_rent)
        })

# Convert to DataFrame
df = pd.DataFrame(all_rows)

# Save historical dataset
df.to_csv("historical_rent.csv", index=False)
print("📄 Saved historical data → historical_rent.csv")

# -------------------------------------------
# STEP 2: Prophet Forecasting
# -------------------------------------------

print("\n🔮 Starting forecasting for each county...\n")

results = []

counties = df["County"].unique()
LAST_YEAR = END_YEAR     # = 2023

for county in counties:

    county_df = df[df["County"] == county].copy()

    # Prophet requires ds + y
    county_df["ds"] = pd.to_datetime(county_df["Year"].astype(str) + "-01-01")
    county_df["y"] = county_df["MedianRent"]

    # At least 3 years required
    if len(county_df) < 3:
        print(f"⚠️ Not enough data for {county}. Skipping.")
        continue

    print(f"✨ Forecasting: {county}")

    model = Prophet(yearly_seasonality=True)
    model.fit(county_df)

    # Forecast future years
    future = model.make_future_dataframe(periods=FORECAST_YEARS, freq="Y")
    forecast = model.predict(future)

    # FIX DIP: Remove any forecasted rows for years ≤ 2023
    forecast["year"] = forecast["ds"].dt.year
    forecast = forecast[forecast["year"] > LAST_YEAR]

    # Clean the forecast output
    temp = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].copy()
    temp["County"] = county

    results.append(temp)

# -------------------------------------------
# STEP 3: Save Forecast Output
# -------------------------------------------

final = pd.concat(results)
final.columns = ["Ds", "Yhat", "Yhat Lower", "Yhat Upper", "County"]

final.to_csv("rent_forecast_results.csv", index=False)

print("\n✅ Saved forecast → rent_forecast_results.csv")
print("🎉 DONE!")
