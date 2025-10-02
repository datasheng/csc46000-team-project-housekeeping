import requests
import datetime
import pandas as pd
from bs4 import BeautifulSoup
## Doesn't shorten phrases
pd.set_option("display.max_colwidth", None)

# grab the page
url = "https://www.ccny.cuny.edu/registrar/fall"
page = requests.get(url)

# parse the HTML with the built-in parser
soup = BeautifulSoup(page.content, "html.parser")

# pull out all the table cells (<td>)
cells = [td.get_text(strip=True) for td in soup.find("table").find_all("td")]

# this will hold our clean rows
rows = []

# every 3 cells = date, day-of-week, description
for i in range(0, len(cells) - 2, 3):
    date_str, dow, text = cells[i], cells[i+1], cells[i+2]

    # skip ranges like "Aug 25 - 31"
    if "-" in date_str:
        continue

    # try to turn "August 24" into a real date
    try:
        date = datetime.datetime.strptime(date_str + " 2021", "%B %d %Y").date()
    except ValueError:
        continue

    rows.append([date, dow, text])

# build table with pandas
df = pd.DataFrame(rows, columns=["date", "dow", "description"]).set_index("date")

# sort by date so it's in order
df = df.sort_index()

# show it nicely in terminal
print(df)

# also save to a CSV file
df.to_csv("ccny_fall_schedule.csv")
