import pandas as pd
import numpy as np
import requests

# ==============================
# CONFIG
# ==============================
FRED_API_KEY = "dc98532537e060468372aca6d91d97f4"
FRED_SERIES = "MORTGAGE30US"

RENT_FILE = "historical_rent.csv"
HOUSE_FILE = "house_price_yearly.csv"

DISCOUNT_RATE = 0.03
YEARS = 30   # <-- use 30 years for realistic break-even


# ==============================
# GET MORTGAGE RATE FROM FRED
# ==============================
print("\n📡 Getting latest mortgage rate from FRED...")

url = f"https://api.stlouisfed.org/fred/series/observations?series_id={FRED_SERIES}&api_key={FRED_API_KEY}&file_type=json"
response = requests.get(url)
data = response.json()["observations"]

df_mort = pd.DataFrame(data)
df_mort["value"] = df_mort["value"].astype(float)
mortgage_rate = df_mort.iloc[-1]["value"]

print(f"📌 Mortgage Rate (FRED): {mortgage_rate}%\n")


# ==============================
# LOAD RENT & HOUSE DATA
# ==============================
rent_df = pd.read_csv(RENT_FILE)
house_df = pd.read_csv(HOUSE_FILE)

rent_df["Year"] = rent_df["Year"].astype(int)
house_df["YearNum"] = house_df["YearNum"].astype(int)

counties = sorted(rent_df["County"].unique())
results = []


# ==============================
# FUNCTION: NPV
# ==============================
def discount(value, year):
    return value / ((1 + DISCOUNT_RATE) ** year)


# ==============================
# MAIN LOOP
# ==============================
for county in counties:

    rent_c = rent_df[rent_df["County"] == county].sort_values("Year")
    house_c = house_df[house_df["County"] == county].sort_values("YearNum")

    if len(rent_c) < 3 or len(house_c) == 0:
        continue

    # Most recent rent & house value
    rent_start = rent_c.iloc[-1]["MedianRent"]
    purchase_price = house_c.iloc[-1]["medianHousePrice"]

    # Mortgage setup
    r_monthly = mortgage_rate / 100 / 12
    n_months = 30 * 12
    monthly_payment = purchase_price * (r_monthly * (1 + r_monthly)**n_months) / ((1 + r_monthly)**n_months - 1)
    property_tax = purchase_price * 0.014  # annual

    # Tracking cumulative costs
    cum_rent = 0
    cum_buy = 0

    breakeven_year = None
    remaining_balance = purchase_price

    for year in range(1, YEARS + 1):

        # --- Rent grows 3% ---
        annual_rent = rent_start * (1.03 ** (year - 1))
        cum_rent += discount(annual_rent, year)

        # --- Mortgage interest & equity ---
        interest_year = 0
        principal_year = 0

        for m in range(12):
            interest_payment = remaining_balance * r_monthly
            principal_payment = monthly_payment - interest_payment

            interest_year += interest_payment
            principal_year += principal_payment

            remaining_balance -= principal_payment

        # Net cost = interest + tax - equity
        net_buy_cost = interest_year + property_tax - principal_year
        cum_buy += discount(net_buy_cost, year)

        # --- Check break-even ---
        if breakeven_year is None and cum_buy <= cum_rent:
            breakeven_year = year

    results.append({
        "County": county,
        "NPV_Rent_10yr": round(cum_rent, 2),
        "NPV_Buy_10yr": round(cum_buy, 2),
        "Difference_BuyMinusRent": round(cum_buy - cum_rent, 2),
        "Better_Option": "Buying" if cum_buy < cum_rent else "Renting",
        "Breakeven_Year": breakeven_year if breakeven_year is not None else "None"
    })


# ==============================
# SAVE OUTPUT
# ==============================
df_results = pd.DataFrame(results)
df_results.to_csv("npv_results.csv", index=False)

print("\n📁 Saved npv_results.csv")
print("✅ Finished buy-vs-rent equity analysis!\n")
