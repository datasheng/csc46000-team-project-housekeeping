import pandas as pd

#For Rent File
fileName="./CSVs/NYSsingleBedCountyDF.csv"
df=pd.read_csv(fileName)
df["RegionName"]=df["RegionName"].str.replace(r" County$", "", regex=True)
df.to_csv("./AllResults/RentData.csv")
#For Buy File
fileName2="./CSVs/NYSsingleFamilyMetroDF.csv"
df2=pd.read_csv(fileName2)
df2["RegionName"]=df2["RegionName"].str.replace(r" ,NY$", "", regex=True)
df2.to_csv("./AllResults/BuyData.csv")