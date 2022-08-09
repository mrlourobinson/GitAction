from bs4 import BeautifulSoup
import requests
import pandas as pd

import requests
page = requests.get("https://www.nimblefins.co.uk/average-cost-electricity-kwh-uk")

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find('h2', string='Unit Cost of Electricity per kWh, by UK Region')
table = title.find_next('table')

df = pd.read_html(str(table),  flavor='html5lib')[0]

print(df[df['Area'] == 'Yorkshire'])