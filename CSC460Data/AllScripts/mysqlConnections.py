import pandas as pd
from sqlalchemy import create_engine, text

engine=create_engine("mysql+mysqlconnector://memyselfi:mypassword@csc460_database:3306/proj_database")

init_commands= [
    "CREATE DATABASE IF NOT EXISTS proj_database;",
    "USE proj_database;",
    #"CREATE TABLE IF NOT EXISTS Rent(CountyName VARCHAR(50) PRIMARY KEY, Month VARCHAR(20), MedianPrice FLOAT);",
    #"CREATE TABLE IF NOT EXISTS Housing(CountyName VARCHAR(50) PRIMARY KEY, Month VARCHAR(20), MedianPrice FLOAT);",
    #"CREATE TABLE IF NOT EXISTS ConsumptionRate(CountyName VARCHAR(50) PRIMARY KEY, Year INT, ConsumptionRate FLOAT);",
    #"CREATE TABLE IF NOT EXISTS PropertyTaxes(CountyName VARCHAR(50) PRIMARY KEY, Year INT, TaxRate FLOAT);",
    "CREATE TABLE IF NOT EXISTS Counties(Countyid INT AUTO_INCREMENT PRIMARY KEY , CountyName VARCHAR(50));",
    "INSERT INTO Counties(CountyName) VALUES ('Albany'), ('Allegany'), ('Bronx'), ('Broome'), ('Cattaraugus'), ('Cayuga'), ('Chautauqua'), ('Chemung'), ('Chenango'), ('Clinton'), ('Columbia'), ('Cortland'), ('Delaware'), ('Dutchess'), ('Erie'), ('Essex'), ('Franklin'), ('Fulton'), ('Genesee'), ('Greene'), ('Hamilton'), ('Herkimer'), ('Jefferson'), ('Kings'), ('Lewis'), ('Livingston'), ('Madison'), ('Monroe'), ('Montgomery'), ('Nassau'), ('New York'), ('Niagara'), ('Oneida'), ('Ontario'), ('Onondaga'), ('Orange'), ('Orleans'), ('Oswego'), ('Otsego'), ('Putnam'), ('Queens'), ('Rensselaer'), ('Richmond'), ('Rockland'), ('St. Lawrence'), ('Saratoga'), ('Schenectady'), ('Schoharie'), ('Schuyler'), ('Seneca'), ('Steuben'), ('Suffolk'), ('Sullivan'), ('Tioga'), ('Tompkins'), ('Ulster'), ('Warren'), ('Washington'), ('Wayne'), ('Westchester'), ('Wyoming'), ('Yates');"
]

with engine.connect() as con:
    for cmd in init_commands:
        con.execute(text(cmd))
    con.commit()

try:
    df1=pd.read_csv('./AllResults/countyData.csv')
except:
    df1=pd.read_csv('./BackupData/countyData.csv')

try:
    df2=pd.read_csv('./AllResults/nysData.csv')
except:
    df2=pd.read_csv('./BackupData/nysData.csv')

try:
    df3=pd.read_csv('./AllResults/propertyTaxPerCounty10years.csv')
except:
    df3=pd.read_csv('./BackupData/propertyTaxPerCounty10years.csv')

df4=pd.read_csv('./AllResults/BuyData.csv')
df5=pd.read_csv('./AllResults/RentData.csv')
df6=pd.read_csv('./AllResults/rent_forecasts.csv')
df7=pd.read_csv('./AllResults/mortgageRates.csv')

df1.to_sql('Consumption_Data_Per_County', con=engine, if_exists='append', index='id')
df2.to_sql('Consumption_Data_Per_Year', con=engine, if_exists='append', index='id')
df3.to_sql('Property_Tax_Per_County', con=engine, if_exists='append', index='id')
df4.to_sql('BuyData', con=engine, if_exists='append', index='id')
df5.to_sql('RentData', con=engine, if_exists='append', index='id')
df6.to_sql("Rent_Forecasts", con=engine, if_exists='append', index='id')
df7.to_sql("Mortgage_Rates", con=engine, if_exists='append', index='id')