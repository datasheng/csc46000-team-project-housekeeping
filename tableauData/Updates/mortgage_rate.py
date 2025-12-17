import requests
import pandas as pd

API_KEY = "dc98532537e060468372aca6d91d97f4"
SERIES_ID = "MORTGAGE30US"

url = f"https://api.stlouisfed.org/fred/series/observations?series_id={SERIES_ID}&api_key={API_KEY}&file_type=json"

response = requests.get(url)
data = response.json()["observations"]

df = pd.DataFrame(data)
df["value"] = df["value"].astype(float)

latest_rate = df.iloc[-1]["value"]

print("Latest 30-year mortgage rate:", latest_rate)
