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
augment_stats_temp = []
for element in soup.findAll(attrs={'class': 'flex items-center justify-end px-[14px] css-y99kx2'}):
    augment_stats_temp.append(element.text)

# top4 and placement have the exact same class name, so I have to separate the two from the temp array
augment_stats_placement = []
augment_stats_top4 = []
for i in range(0, len(augment_stats_temp), 2):
    augment_stats_placement.append(augment_stats_temp[i])
for i in range(1, len(augment_stats_temp), 2):
    augment_stats_top4.append(augment_stats_temp[i])

# get the stat of how frequently an augment is chosen
augment_stats_freq = []
for element in soup.findAll(attrs={'class': 'flex items-center justify-end px-[14px] css-1ise070'}):
    augment_stats_freq.append(element.text)

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

# this is super inefficent but I don't really want to think of another way since it works fine
for i in range(len(augment_names)):
    augment_collection = {}
    augment_collection["augment"] = augment_names[i]
    augment_collection["placement"] = augment_stats_placement[i]
    augment_collection["top4%"] = augment_stats_top4[i]
    augment_collection["freqency"] = augment_stats_freq[i]
    augment_collection["win%"] = augment_stats_win[i]
    db.augments.insert_one(augment_collection)

for i in range(len(champ_name)):
    augment_collection = {}
    augment_collection["unit"] = champ_name[i]
    augment_collection["placement"] = champ_placement[i]
    augment_collection["playrate"] = champ_playrate[i]
    db.units.insert_one(augment_collection)