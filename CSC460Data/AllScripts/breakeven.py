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

DISCOUNT_RATE = 0.03   # 3% discount rate
YEARS = 10             # 10-year NPV horizon


# ==============================
# 1. GET MORTGAGE RATE FROM FRED
# ==============================
print("\n📡 Getting latest mortgage rate from FRED...")

fred_url = (
    f"https://api.stlouisfed.org/fred/series/observations"
    f"?series_id={FRED_SERIES}&api_key={FRED_API_KEY}&file_type=json"
)

response = requests.get(fred_url)
data = response.json()["observations"]

df_mort = pd.DataFrame(data)
df_mort["value"] = df_mort["value"].astype(float)

mortgage_rate = df_mort.iloc[-1]["value"]
print(f"📌 Mortgage Rate (FRED): {mortgage_rate}%\n")


# ==============================
# 2. LOAD RENT + HOUSE PRICE DATA
# ==============================
rent_df = pd.read_csv(RENT_FILE)
house_df = pd.read_csv(HOUSE_FILE)

# consistent col names
rent_df["Year"] = rent_df["Year"].astype(int)
house_df["YearNum"] = house_df["YearNum"].astype(int)


# ==============================
# 3. UNIQUE COUNTIES
# ==============================
counties = sorted(rent_df["County"].unique())
results = []


# ==============================
# 4. LOOP THROUGH COUNTIES
# ==============================
def npv_calc(cashflows, discount_rate):
    return sum(cf / ((1 + discount_rate) ** t) for t, cf in enumerate(cashflows, start=1))


print("🔄 Running NPV analysis for all counties...\n")

for county in counties:

    # ----- Rent Data -----
    rent_c = rent_df[rent_df["County"] == county].sort_values("Year")

    if len(rent_c) < 3:
        print(f"⚠️ Skipping {county} — not enough rent data.\n")
        continue

    rent_start = rent_c.iloc[-1]["MedianRent"]  # most recent rent

    # assume 3% yearly increase in rent
    rent_forecast = [rent_start * (1.03 ** i) for i in range(YEARS)]
    npv_rent = npv_calc(rent_forecast, DISCOUNT_RATE)

    # ----- House Price Data -----
    house_c = house_df[house_df["County"] == county].sort_values("YearNum")

    if len(house_c) == 0:
        print(f"⚠️ Skipping {county} — no house price data.\n")
        continue

    purchase_price = house_c.iloc[-1]["medianHousePrice"]

    # mortgage 30-year fixed, assume fixed payment:
    r = mortgage_rate / 100 / 12
    n = 30 * 12

    monthly_payment = purchase_price * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    yearly_payment = monthly_payment * 12

    # property tax estimate 1.4%
    property_tax = purchase_price * 0.014

    buy_costs = [(yearly_payment + property_tax) for _ in range(YEARS)]
    npv_buy = npv_calc(buy_costs, DISCOUNT_RATE)

    diff = npv_buy - npv_rent
    better = "Buying" if diff < 0 else "Renting"

    # store row
    results.append({
        "County": county,
        "NPV_Rent_10yr": round(npv_rent, 2),
        "NPV_Buy_10yr": round(npv_buy, 2),
        "Difference_BuyMinusRent": round(diff, 2),
        "Better_Option": better
    })


# ==============================
# 5. SAVE RESULTS FOR TABLEAU
# ==============================
results_df = pd.DataFrame(results)
results_df.to_csv("npv_results.csv", index=False)

print("\n📁 Saved: npv_results.csv")
print("✅ Completed NPV analysis for all counties!\n")