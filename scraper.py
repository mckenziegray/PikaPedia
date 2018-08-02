import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
response = requests.get(url)
response.text[:100] # Access the HTML with the text property

#print(response.text[:100]) # Access the HTML with the text property

html_string = response.text[:100] # Access the HTML with the text property

soup = BeautifulSoup(html_string, 'lxml') # Parse the HTML as a string

table = soup.find_all('table')[0] # Grab the first table

new_table = pd.DataFrame(columns=range(0,2), index = [0]) # I know the size 

row_marker = 0
for row in table.find_all('tr'):
    column_marker = 0
    columns = row.find_all('td')
    for column in columns:
        new_table.iat[row_marker,column_marker] = column.get_text()
        column_marker += 1
                       
print(new_table)
