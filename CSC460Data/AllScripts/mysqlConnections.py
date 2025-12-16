import pandas as pd
from sqlalchemy import create_engine, text
import mysql.connector

DB_HOST = "csc460_database"
DB_USER = "memyselfi"
DB_PASS = "mypassword"
DB_NAME = "proj_database"

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
    )
conn.close()
print("Database is ready")

engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}")

init_commands= [
    #"CREATE TABLE IF NOT EXISTS Rent(CountyName VARCHAR(50) PRIMARY KEY, Month VARCHAR(20), MedianPrice FLOAT);",
    #"CREATE TABLE IF NOT EXISTS Housing(CountyName VARCHAR(50) PRIMARY KEY, Month VARCHAR(20), MedianPrice FLOAT);",
    #"CREATE TABLE IF NOT EXISTS ConsumptionRate(CountyName VARCHAR(50) PRIMARY KEY, Year INT, ConsumptionRate FLOAT);",
    #"CREATE TABLE IF NOT EXISTS PropertyTaxes(CountyName VARCHAR(50) PRIMARY KEY, Year INT, TaxRate FLOAT);",
    "CREATE TABLE IF NOT EXISTS Counties(Countyid INT AUTO_INCREMENT PRIMARY KEY , CountyName VARCHAR(50) UNIQUE);",
    """
    INSERT IGNORE INTO Counties(CountyName) 
    VALUES ('Albany'), ('Allegany'), ('Bronx'), ('Broome'), ('Cattaraugus'), ('Cayuga'), 
    ('Chautauqua'), ('Chemung'), ('Chenango'), ('Clinton'), ('Columbia'), ('Cortland'), 
    ('Delaware'), ('Dutchess'), ('Erie'), ('Essex'), ('Franklin'), ('Fulton'), 
    ('Genesee'), ('Greene'), ('Hamilton'), ('Herkimer'), ('Jefferson'), ('Kings'), 
    ('Lewis'), ('Livingston'), ('Madison'), ('Monroe'), ('Montgomery'), ('Nassau'), 
    ('New York'), ('Niagara'), ('Oneida'), ('Ontario'), ('Onondaga'), ('Orange'), 
    ('Orleans'), ('Oswego'), ('Otsego'), ('Putnam'), ('Queens'), ('Rensselaer'), 
    ('Richmond'), ('Rockland'), ('St. Lawrence'), ('Saratoga'), ('Schenectady'), ('Schoharie'), 
    ('Schuyler'), ('Seneca'), ('Steuben'), ('Suffolk'), ('Sullivan'), ('Tioga'), 
    ('Tompkins'), ('Ulster'), ('Warren'), ('Washington'), ('Wayne'), ('Westchester'), ('Wyoming'), ('Yates');
    """
]

with engine.connect() as con:
    for cmd in init_commands:
        con.execute(text(cmd))
    con.commit()


def try_except(orig, backup):
    try:
        return pd.read_csv(orig)
    except:
        if backup:
            return pd.read_csv(backup)

df1=try_except('./AllResults/countyData.csv', './BackupData/countyData.csv')
df2=try_except('./AllResults/nysData.csv', './BackupData/nysData.csv')
df3=try_except('./AllResults/propertyTaxPerCounty10years.csv', './BackupData/propertyTaxPerCounty10years.csv')

df4=pd.read_csv('./AllResults/BuyData.csv')
df5=pd.read_csv('./AllResults/RentData.csv')
df6=pd.read_csv('./AllResults/rent_forecasts.csv')
df7=pd.read_csv('./AllResults/mortgageRates.csv')
df8=pd.read_csv('./tableauData/ACS_nys_housing_acs_2015_2023.csv')

df1.to_sql('Consumption_Data_Per_County', con=engine, if_exists='replace', index='id')
df2.to_sql('Consumption_Data_Per_Year', con=engine, if_exists='replace', index='id')
df3.to_sql('Property_Tax_Per_County', con=engine, if_exists='replace', index='id')
df4.to_sql('BuyData', con=engine, if_exists='replace', index='id')
df5.to_sql('RentData', con=engine, if_exists='replace', index='id')
df6.to_sql("Rent_Forecasts", con=engine, if_exists='replace', index='id')
df7.to_sql("Mortgage_Rates", con=engine, if_exists='replace', index='id')
df8.to_sql("ACS_nys_housing_acs_2015_2023", con=engine, if_exists='replace', index='id')

print("Database successfully populated")

