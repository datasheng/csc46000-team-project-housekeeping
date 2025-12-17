import pandas as pd
import numpy as np
import requests

# ========================
# CONFIG
# ========================
FRED_API_KEY = "dc98532537e060468372aca6d91d97f4"
FRED_SERIES = "MORTGAGE30US"

RENT_FILE = "processed_rent_forecast.csv"
HOUSE_FILE = "house_price_yearly.csv"

DISCOUNT_RATE = 0.03


# ========================
# GET MORTGAGE RATE
# ========================
print("\n📡 Getting latest mortgage rate from FRED...")

url = f"https://api.stlouisfed.org/fred/series/observations?series_id={FRED_SERIES}&api_key={FRED_API_KEY}&file_type=json"
mort_data = requests.get(url).json()["observations"]

df_mort = pd.DataFrame(mort_data)
df_mort["value"] = df_mort["value"].astype(float)
mortgage_rate = df_mort.iloc[-1]["value"]

print(f"📌 Mortgage Rate Loaded: {mortgage_rate}%\n")


# ========================
# LOAD DATA
# ========================
rent_df = pd.read_csv(RENT_FILE)
rent_df["year"] = rent_df["year"].astype(int)

house_df = pd.read_csv(HOUSE_FILE)
house_df["YearNum"] = house_df["YearNum"].astype(int)

counties = sorted(rent_df["County"].unique())

results = []


def discount(value, year):
    return value / ((1 + DISCOUNT_RATE) ** year)


# ========================
# MAIN LOOP
# ========================
for county in counties:

    rent_c = rent_df[rent_df["County"] == county].sort_values("year")

    # auto-detect FORECAST YEARS
    YEARS = len(rent_c)
    if YEARS < 2:
        print(f"⚠️ Not enough forecast for {county}, skipping.")
        continue

    # convert cumulative → yearly rent
    rent_c["Yearly_Rent"] = rent_c["Accumulated_Rent_yearly"].diff()
    rent_c.iloc[0, rent_c.columns.get_loc("Yearly_Rent")] = rent_c.iloc[0]["Accumulated_Rent_yearly"]

    house_c = house_df[house_df["County"] == county]
    if len(house_c) == 0:
        print(f"⚠️ No house price for {county}, skipping.")
        continue

    purchase_price = house_c.iloc[-1]["medianHousePrice"]

    # mortgage math
    r_monthly = mortgage_rate / 100 / 12
    n_months = 30 * 12
    monthly_payment = purchase_price * (r_monthly * (1 + r_monthly)**n_months) / ((1 + r_monthly)**n_months - 1)
    property_tax = purchase_price * 0.014

    cum_rent = 0
    cum_buy = 0
    remaining_balance = purchase_price
    breakeven_year = None

    for year in range(1, YEARS + 1):

        # ----- Rent -----
        annual_rent = rent_c.iloc[year - 1]["Yearly_Rent"]
        cum_rent += discount(annual_rent, year)

        # ----- Buy -----
        interest_year = 0
        principal_year = 0

        for _ in range(12):
            interest_payment = remaining_balance * r_monthly
            principal_payment = monthly_payment - interest_payment

            interest_year += interest_payment
            principal_year += principal_payment
            remaining_balance -= principal_payment

        net_buy_cost = interest_year + property_tax - principal_year
        cum_buy += discount(net_buy_cost, year)

        if breakeven_year is None and cum_buy <= cum_rent:
            breakeven_year = year

    results.append({
        "County": county,
        "Forecast_Years": YEARS,
        "NPV_Rent": round(cum_rent, 2),
        "NPV_Buy": round(cum_buy, 2),
        "Difference_BuyMinusRent": round(cum_buy - cum_rent, 2),
        "Better_Option": "Buying" if cum_buy < cum_rent else "Renting",
        "Breakeven_Year": breakeven_year if breakeven_year else "None (within forecast)"
    })


# Save final output
df_results = pd.DataFrame(results)
df_results.to_csv("npv_results.csv", index=False)

print("📁 Saved: npv_results.csv")
print("✅ NPV generated for actual forecast horizon per county!")
