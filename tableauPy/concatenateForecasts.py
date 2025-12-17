import pandas as pd

# load
buy = pd.read_csv("tableauData/pivotBuyData.csv")
forecast = pd.read_csv("tableauData/forcast_housePrice_data.csv")

# parse dates
buy["Date"] = pd.to_datetime(buy["Date"])
forecast["Year"] = pd.to_datetime(forecast["Year"])

# filter forecast to 2023+
forecast = forecast[forecast["Year"].dt.year >= 2023]

# rename + align columns
forecast = forecast.rename(columns={
    "Year": "Date",
    "County": "MunicipalCodeFIPS",   # only if this is your join key
    "medianHousePrice": "MedianValue"
})

# add missing columns so schemas match
for col in buy.columns:
    if col not in forecast.columns:
        forecast[col] = None

forecast = forecast[buy.columns]

# concatenate
combined = pd.concat([buy, forecast], ignore_index=True)

# save
combined.to_csv("tableauData/combined_buy_forecast.csv", index=False)
