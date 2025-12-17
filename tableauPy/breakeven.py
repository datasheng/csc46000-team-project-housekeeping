import pandas as pd

# ----------------------------
# CONFIG
# ----------------------------
INPUT_FILE = "tableauData/ACS_nys_housing_acs_2015_2023.csv"
OUTPUT_FILE = "tableauData/break_even_realistic.csv"
SAVINGS = 250_000  # upfront savings

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv(INPUT_FILE)

# Assume Owner_Cost_With_Mortgage is annual; if monthly, multiply by 12
df['Owner_Cost_Annual'] = df['Owner_Cost_With_Mortgage']

# Sort by County and Year
df = df.sort_values(['County', 'Year'])

# ----------------------------
# CUMULATIVE RENT
# ----------------------------
df['Cumulative_Rent'] = df.groupby('County')['Median_Gross_Rent'].cumsum()

# ----------------------------
# CUMULATIVE EQUITY / OWNER COST CONSIDERING SAVINGS
# ----------------------------
df['Cumulative_Equity'] = 0  # initialize

for county, group in df.groupby('County'):
    group = group.sort_values('Year')
    equity_list = []

    first_row = group.iloc[0]
    house_price = first_row['Median_Home_Value']
    owner_costs = group['Owner_Cost_Annual'].tolist()

    if SAVINGS >= house_price:
        # Savings fully pays the house upfront
        remaining_savings = SAVINGS - house_price
        cum_equity = house_price + remaining_savings
        for cost in owner_costs:
            equity_list.append(cum_equity)
            cum_equity += cost  # add yearly owner cost to equity
    else:
        # Cannot fully pay house; assume no break-even
        equity_list = [0]*len(owner_costs)

    df.loc[group.index, 'Cumulative_Equity'] = equity_list

# ----------------------------
# NET DIFFERENCE
# ----------------------------
df['Net_Difference'] = df['Cumulative_Rent'] - df['Cumulative_Equity']

# ----------------------------
# SCALE FOR TABLEAU
# ----------------------------
df['Cumulative_Rent_k'] = df['Cumulative_Rent'] / 1000
df['Cumulative_Equity_k'] = df['Cumulative_Equity'] / 1000
df['Net_Difference_k'] = df['Net_Difference'] / 1000

# ----------------------------
# EXPORT FOR TABLEAU
# ----------------------------
df.to_csv(OUTPUT_FILE, index=False)

print(f"Break-even CSV generated: {OUTPUT_FILE}")
