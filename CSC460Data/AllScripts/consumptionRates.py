import pandas as pd
from bs4 import BeautifulSoup
import requests
import numpy as np

url='https://livingwage.mit.edu/counties/' 

start=36001
end=36123
codes=[]
for i in range(start, end+1, 2):
    codes.append(str(i))

r=requests.get('https://livingwage.mit.edu/counties/36001')
html_doc=r.text
soup=BeautifulSoup(html_doc, 'html.parser')

expenseTable=soup.find_all(class_='results_table table-striped expense_table')[0]
col_names=[]

for col_name in expenseTable.find_all(class_='text'):
    col_names.append(col_name.text)
#print(col_names)

requestPerCounty=[]
for code in codes:
    requestPerCounty.append(BeautifulSoup(requests.get('https://livingwage.mit.edu/counties/'+code).text))

tablePerCounty=[]
for request in requestPerCounty:
    tablePerCounty.append(request.find_all(class_='results_table table-striped expense_table')[0])

dollarAmount=[]
for table in tablePerCounty:
    total=[]
    for  trow in table.find_all('tr')[2:]:
        total.append(trow.find_all('td')[1].text.strip())
    dollarAmount.append(total)

nys_counties = ["Albany", "Allegany", "Bronx", "Broome", "Cattaraugus", "Cayuga", "Chautauqua", "Chemung", "Chenango", "Clinton", "Columbia", "Cortland", 
                "Delaware", "Dutchess", "Erie", "Essex", "Franklin", "Fulton", "Genesee", "Greene", "Hamilton", "Herkimer", "Jefferson", "Kings", "Lewis", 
                "Livingston", "Madison", "Monroe", "Montgomery", "Nassau", "New York", "Niagara", "Oneida", "Onondaga", "Ontario", "Orange", "Orleans", 
                "Oswego", "Otsego", "Putnam", "Queens", "Rensselaer", "Richmond", "Rockland", "St. Lawrence", "Saratoga", "Schenectady", "Schoharie", 
                "Schuyler", "Seneca", "Steuben", "Suffolk", "Sullivan", "Tioga", "Tompkins", "Ulster", "Warren", "Washington", "Wayne", "Westchester", 
                "Wyoming", "Yates"]

data=np.array(dollarAmount)
df=pd.DataFrame(data, columns=col_names)
df['County']=nys_counties
df.set_index('County', inplace=True)
pd.set_option('display.max_rows', None)  

for col in df.columns:
    if (col != 'County'):
        df[col]=df[col].str.replace(r'[$,]', '', regex=True).astype(float)


df.to_csv('./AllResults/countyData.csv')

#Now ill do the same for the past 10 years


years=['2025', '2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015']


links=['https://web.archive.org/web/20151220151322/https://livingwage.mit.edu/states/36',
       'https://web.archive.org/web/20161207171550/https://livingwage.mit.edu/states/36',
       'https://web.archive.org/web/20171207053953/https://livingwage.mit.edu/states/36',
       'https://web.archive.org/web/20181026231852/https://livingwage.mit.edu/states/36',
       'https://web.archive.org/web/20190811183231/http://livingwage.mit.edu/states/36',
       'https://web.archive.org/web/20201124071353/https://livingwage.mit.edu/states/36',
       'https://web.archive.org/web/20211016060013/https://livingwage.mit.edu/states/36',
       'https://web.archive.org/web/20221223191058/https://livingwage.mit.edu/states/36',
       'https://web.archive.org/web/20231202131633/https://livingwage.mit.edu/states/36',
       'https://web.archive.org/web/20241230163723/https://livingwage.mit.edu/states/36',
       'https://livingwage.mit.edu/states/36'
       ]

requestPerYear=[]
for link in links:
    requestPerYear.append(BeautifulSoup(requests.get(link).text, 'html.parser'))

tablePerYear=[]
for request in requestPerYear:
    try:
        tablePerYear.append(request.find_all(class_='table table-striped table-condensed expenses_table')[0])
    except:
        tablePerYear.append(request.find_all(class_='results_table table-striped expense_table')[0])

count=0
dollarAmountperYear=[]
for table in tablePerYear:
    total=[]
    if count>4:
        for  trow in table.find_all('tr')[2:]:
            total.append(trow.findAll('td')[1].text.strip())
    else:
        for  trow in table.find_all('tr')[1:]:
            total.append(trow.findAll('td')[1].text.strip())
    count+=1
    dollarAmountperYear.append(total)

data2=np.array(dollarAmountperYear[9:11])
data2=data2[::-1]
df2=pd.DataFrame(data2, columns=col_names)

col_names2=col_names.copy()
col_names2.remove('Internet & Mobile')
data3=np.array(dollarAmountperYear[6:9])
data3=data3[::-1]
df3=pd.DataFrame(data3, columns=col_names2)

col_names3=col_names2.copy()
col_names3.remove('Civic')
data4=np.array(dollarAmountperYear[:6])
data4=data4[::-1]
df4=pd.DataFrame(data4, columns=col_names3)


allYears = pd.concat([df2, df3, df4], axis=0)
dollarAmountperYear

allYears['year']=years
allYears.set_index('year', inplace=True)

for col in allYears.columns:
    if (col != 'year'):
        allYears[col]=allYears[col].str.replace(r'[$,]', '', regex=True).astype(float)
        allYears[col]=allYears[col].fillna(allYears[col].mean())

allYears=allYears.iloc[::-1].reset_index(drop=True)

allYears.to_csv('./AllResults/nysData.csv')
allYears