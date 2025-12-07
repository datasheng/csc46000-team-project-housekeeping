import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np


links=['https://web.archive.org/web/20151107184144/https://www.tax-rates.org/new_york/property-tax',
    'https://web.archive.org/web/20161118074213/https://www.tax-rates.org/new_york/property-tax',
    'https://web.archive.org/web/20171231105050/https://www.tax-rates.org/new_york/property-tax',
    'https://web.archive.org/web/20181216034723/https://www.tax-rates.org/new_york/property-tax',
    'https://web.archive.org/web/20191223033110/https://www.tax-rates.org/new_york/property-tax',
    'https://web.archive.org/web/20201125165347/https://www.tax-rates.org/new_york/property-tax',
    'https://web.archive.org/web/20211026212201/https://www.tax-rates.org/new_york/property-tax',
    'https://web.archive.org/web/20221208192209/https://www.tax-rates.org/new_york/property-tax',
    'https://web.archive.org/web/20231203074442/https://www.tax-rates.org/new_york/property-tax',
    'https://web.archive.org/web/20241226135411/https://www.tax-rates.org/new_york/property-tax',
    'https://www.tax-rates.org/new_york/property-tax'
]

years=['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
nys_counties = ["Albany", "Allegany", "Bronx", "Broome", "Cattaraugus", "Cayuga", "Chautauqua", "Chemung", "Chenango", "Clinton", "Columbia", "Cortland", 
                "Delaware", "Dutchess", "Erie", "Essex", "Franklin", "Fulton", "Genesee", "Greene", "Hamilton", "Herkimer", "Jefferson", "Kings", "Lewis", 
                "Livingston", "Madison", "Monroe", "Montgomery", "Nassau", "New York", "Niagara", "Oneida", "Onondaga", "Ontario", "Orange", "Orleans", 
                "Oswego", "Otsego", "Putnam", "Queens", "Rensselaer", "Richmond", "Rockland", "St. Lawrence", "Saratoga", "Schenectady", "Schoharie", 
                "Schuyler", "Seneca", "Steuben", "Suffolk", "Sullivan", "Tioga", "Tompkins", "Ulster", "Warren", "Washington", "Wayne", "Westchester", 
                "Wyoming", "Yates"]

allRequests=[]
for link in links:
    r=requests.get(link)
    html_doc=BeautifulSoup(r.text)
    allRequests.append(html_doc)

amountPerYear=[]
for r in allRequests:
    table=r.find_all(class_='propertyTaxTable')[1]
    money=table.find_all('td')
    total=[]
    for m in money[:-1]:
         total.append([t.strip() for t in m.strings if t.strip()][1])
    amountPerYear.append(total)

data=np.array(amountPerYear)
df=pd.DataFrame(data, years).T
df['County']=nys_counties
df.set_index('County', inplace=True)


for col in df.columns:
    if (col != 'County'):
        df[col]=df[col].str.replace(r'[$,]', '', regex=True).astype(float)
df.to_csv('../AllResults/propertyTaxPerCounty10years.csv')
df.head()
