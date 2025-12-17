import requests
import pandas as pd

API_KEY = "6b31c2d41f669896f9f32d1b16d1a2b38950be89"
years = range(2015, 2024)  # 2015–2023
variables = {
    "Median_Gross_Rent": "B25064_001E",
    "Median_Home_Value": "B25077_001E",
    "Median_Property_Tax": "B25103_001E",
    "Owner_Cost_With_Mortgage": "B25088_001E",
    "Owner_Cost_Without_Mortgage": "B25091_001E"
}

all_data = []

for year in years:
    url = f"https://api.census.gov/data/{year}/acs/acs5"
    params = {
        "get": ",".join(variables.values()) + ",NAME",
        "for": "county:*",
        "in": "state:36",  # New York
        "key": API_KEY
    }
    r = requests.get(url, params=params)
    r.raise_for_status()  # stop if request fails
    data = r.json()
    
    for row in data[1:]:
        county_name = row[-3].replace(" County, New York", "")
        county_data = {
            "Year": year,
            "County": county_name,
            "State": "New York"
        }

        for i, metric in enumerate(variables.keys()):
            county_data[metric] = row[i]
        all_data.append(county_data)

df = pd.DataFrame(all_data)
df.to_csv("tableauData/ACS_nys_housing_acs_2015_2023.csv", index=False)
print(df.head())
