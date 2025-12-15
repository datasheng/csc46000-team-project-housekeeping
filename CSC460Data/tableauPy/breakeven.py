import pandas as pd
import numpy as np

df = pd.read_csv("tableauData/ACS_nys_housing_acs_2015_2023.csv")

# Our initial 250,000
downpayment = 250000 

breakeven_rows = []

for i, row in df.iterrows():
    home_price = row["Median_Home_Value"]
    monthly_rent = row["Median_Gross_Rent"]
    monthly_buy = row["Owner_Cost_With_Mortgage"]


    if monthly_rent <= monthly_buy:
        breakeven_months = np.nan  # never breaks even
    else:
        breakeven_months = downpayment / (monthly_rent - monthly_buy)

    breakeven_rows.append({
        "County": row["County"],
        "Year": row["Year"],
        "Breakeven_Months": breakeven_months,
        "Breakeven_Years": breakeven_months / 12 if breakeven_months else np.nan
    })

breakeven_df = pd.DataFrame(breakeven_rows)
breakeven_df.to_csv("tableauData/breakeven_by_county.csv", index=False)
