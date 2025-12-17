import pandas as pd
import numpy as np
import numpy_financial as npf

# --------------------
# Load data
# --------------------
df = pd.read_csv("tableauData/ACS_nys_housing_acs_2015_2023.csv")
rates = pd.read_csv("AllResults/mortgageRates.csv")
rates.rename(columns={"Mortgage Rate": "Mortgage_Rate"}, inplace=True)
rates["Year"] = rates["Date"].str[:4].astype(int)

# Merge mortgage rates by year
df = df.merge(rates, on="Year", how="left")

# --------------------
# Assumptions
# --------------------
CASH_AVAILABLE = 250_000   # Total cash available for down payment
MIN_DOWN_PCT = 0.20        # Minimum conventional down payment
TERM_YEARS = 30
MONTHS = TERM_YEARS * 12
SELL_COST_PCT = 0.06
DISCOUNT_RATE = 0.07       # Used for NPV
APPRECIATION_RATE = 0.03   # Annual home price growth

# --------------------
# Helper functions
# --------------------
def npv(rate, cash_flows):
    return sum(cf / (1 + rate) ** i for i, cf in enumerate(cash_flows))

def safe_irr(cash_flows):
    cf = np.array(cash_flows, dtype=float)
    if not (np.any(cf > 0) and np.any(cf < 0)):
        return np.nan
    return npf.irr(cf)

def remaining_balance(price, rate, years_elapsed, down_payment):
    loan = price - down_payment
    r = rate / 12
    n = TERM_YEARS * 12
    if loan <= 0:
        return 0
    pmt = loan * (r * (1 + r)**n) / ((1 + r)**n - 1)
    paid_months = min(years_elapsed * 12, n)
    balance = loan * (1 + r)**paid_months - pmt * ((1 + r)**paid_months - 1) / r
    return max(balance, 0)

# --------------------
# Cash flows per county
# --------------------
# Initialize columns
df["Buy_CF"] = np.nan
df["Rent_CF"] = -df["Median_Gross_Rent"] * 12
df["Buy_Eligible"] = True
df["Down_Payment_Used"] = 0

for idx, row in df.iterrows():
    price0 = row["Median_Home_Value"]
    required_down = price0 * MIN_DOWN_PCT
    
    # Check if $250k is enough
    if CASH_AVAILABLE < required_down:
        df.at[idx, "Buy_Eligible"] = False
        df.at[idx, "Buy_CF"] = np.nan
        continue
    
    # Use smaller of $250k or required down
    down_payment = min(CASH_AVAILABLE, required_down)
    df.at[idx, "Down_Payment_Used"] = down_payment
    
    # Calculate mortgage
    mort_rate = row["Mortgage_Rate"]
    loan = price0 - down_payment
    r = mort_rate / 12
    n = TERM_YEARS * 12
    if loan > 0:
        pmt = loan * (r * (1 + r)**n) / ((1 + r)**n - 1)
    else:
        pmt = 0
    
    # Cash flows for 1 year
    buy_cf = -row["Owner_Cost_With_Mortgage"] * 12
    # Subtract down payment only the first year
    if idx == df.index[0]:
        buy_cf -= down_payment
    df.at[idx, "Buy_CF"] = buy_cf

# --------------------
# Final year sale adjustment
# --------------------
# Group by county
for county, g in df.groupby("County"):
    if not g["Buy_Eligible"].all():
        continue
    last_idx = g.index[-1]
    years_held = g.shape[0]
    
    price0 = g.loc[g.index[0], "Median_Home_Value"]
    mort_rate = g.loc[last_idx, "Mortgage_Rate"]
    down_payment = g.loc[g.index[0], "Down_Payment_Used"]
    
    # Sale price with appreciation
    sale_price = price0 * (1 + APPRECIATION_RATE) ** years_held
    remaining_loan = remaining_balance(sale_price, mort_rate, years_held, down_payment)
    
    df.at[last_idx, "Buy_CF"] += (sale_price - remaining_loan - sale_price * SELL_COST_PCT)

# --------------------
# Results per county
# --------------------
results = []
for county, g in df.groupby("County"):
    if not g["Buy_Eligible"].all():
        results.append({
            "County": county,
            "Buy_NPV": np.nan,
            "Rent_NPV": npv(DISCOUNT_RATE, g["Rent_CF"]),
            "Buy_IRR": np.nan,
            "Rent_IRR": safe_irr(g["Rent_CF"]),
            "Buy_Eligible": False
        })
        continue
    
    buy_npv = npv(DISCOUNT_RATE, g["Buy_CF"])
    rent_npv = npv(DISCOUNT_RATE, g["Rent_CF"])
    buy_irr = safe_irr(g["Buy_CF"])
    rent_irr = safe_irr(g["Rent_CF"])
    
    results.append({
        "County": county,
        "Buy_NPV": buy_npv,
        "Rent_NPV": rent_npv,
        "Buy_IRR": buy_irr,
        "Rent_IRR": rent_irr,
        "Buy_Eligible": True
    })

summary = pd.DataFrame(results)

# --------------------
# Export for Tableau
# --------------------
df.to_csv("tableauData/cash_flows_for_tableau.csv", index=False)
summary.to_csv("tableauData/county_buy_vs_rent_summary.csv", index=False)

print("Done! Cash-constrained buy vs rent model complete.")
