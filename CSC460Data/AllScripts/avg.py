import pandas as pd

df=pd.read_csv("BackupData/nysData.csv")
df['total']=(df['Food']+df['Medical']+df['Transportation'] + df['Civic'] + df['Internet & Mobile'] +df['Other'] + df['Annual taxes'] )
print(df)
