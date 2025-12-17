import pandas as pd
from fredapi import Fred

fred = Fred(api_key='bd2983759a4cf1e15823ed3442667fb4') # it's the key from https://fredaccount.stlouisfed.org/apikey
rates = fred.get_series('MORTGAGE30US', observation_start='2015-01-01') #mortgage rate from 2015 to 2025
df_rates = pd.DataFrame(rates, columns=['Mortgage Rate']) # DataFrame for the 'rate dat'
df_rates.index.name = 'Date'
#This is the only thing I edited to create the mortgageRates.csv file
df_rates
abc=pd.DataFrame(df_rates)
print(abc.head())
abc.reset_index(inplace=True)
print(abc.dtypes)
abcd=abc.groupby(abc["Date"].dt.to_period("M"))["Mortgage Rate"].mean().round(2)
abcd.to_csv('./AllResults/mortgageRates.csv')
print(abcd.head())