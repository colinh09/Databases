from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
from pymongo import MongoClient

### get data for all augments ###
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://tactics.tools/augments')

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
# get the names of all the augments
augment_names = []
for element in soup.findAll(attrs={'class': 'flex items-center px-[8px] md:px-[14px] css-cpr46l'}):
    augment_names.append(element.text)

# get the stats of the place statistics (% of top 4s and average place)
augment_stats_place = []
for element in soup.findAll(attrs={'class': 'flex items-center justify-end px-[14px] css-y99kx2'}):
    augment_stats_place.append(element.text)

# get the stat of how frequently an augment is chosen
augment_stats_freq = []
for element in soup.findAll(attrs={'class': 'flex items-center justify-end px-[14px] css-1ise070'}):
    augment_stats_place.append(element.text)

# get the win percentage of the augment (1st place is a win)
augment_stats_win = []
for element in soup.findAll(attrs={'class': 'flex items-center justify-end px-[14px] css-njtzbj'}):
    augment_stats_win.append(element.text)


### get data for all units ###
driver.get('https://tactics.tools/units')
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

# get all of the units' names
champ_name = []
for element in soup.findAll(attrs={'class': 'text-base font-medium whitespace-no-wrap truncate css-l6s31b'}):
    champ_name.append(element.text)

# get the unit's playrate
champ_playrate = []
for element in soup.findAll(attrs={'class': 'w-[34px]'}):
    champ_playrate.append(element.text)

# get the unit's average placement
champ_placement = []
for element in soup.findAll(attrs={'class': 'text-right css-wldxpd'}):
    champ_placement.append(element.text)

conn_str = "mongodb+srv://colin:<password>@cluster0.zqayzpq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str)
db = client.tft
print(augment_names)
db.augments.insert_many(augment_names)
print("Success")
