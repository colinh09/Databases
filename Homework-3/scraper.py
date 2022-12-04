from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
from pymongo import MongoClient
import re

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
    augment_stats_temp.append(re.sub(r'[^0-9.]', '', element.text))

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
    augment_stats_freq.append(re.sub(r'[^0-9]', '', element.text))

# get the win percentage of the augment (1st place is a win)
augment_stats_win = []
for element in soup.findAll(attrs={'class': 'flex items-center justify-end px-[14px] css-njtzbj'}):
    augment_stats_win.append(re.sub(r'[^0-9.]', '', element.text))

# get the stat of the units that have the highest win rate with the augment
# unfortunately, the maker of the website did not put the names of the units, only the source image
# the maker of the website also called a lot of the units by a different name in the source images, so i had to map them all by hand
# therefore, I have to do a (very very annoying) extra work to get the top units
augment_stats_units = []
for element in soup.findAll(attrs={'class': 'flex items-center pl-6 justify-center gap-[5px] px-[14px] css-175tob7'}):
    for element2 in element.findAll('img'):
        augment_stats_units.append(element2['src'])

for i in range(len(augment_stats_units)):
    augment_stats_units[i] = augment_stats_units[i][32:len(augment_stats_units[i]) - 13]
    if (augment_stats_units[i] == 'dragongreen'):
        augment_stats_units[i] = 'shi oh yu'
    if (augment_stats_units[i] == 'dragonearth'):
        augment_stats_units[i] = 'terra'
    if (augment_stats_units[i] == 'dragonpurple'):
        augment_stats_units[i] = 'syfen'
    if (augment_stats_units[i] == 'dragonblue'):
        augment_stats_units[i] = 'daeja'
    if (augment_stats_units[i] == 'aquaticdragon'):
        augment_stats_units[i] = 'sohm'
    if (augment_stats_units[i] == 'dragongold'):
        augment_stats_units[i] = 'idas'
    if (augment_stats_units[i] == 'dragonguild'):
        augment_stats_units[i] = 'zippy'
    if (augment_stats_units[i] == 'dragonswain'):
        augment_stats_units[i] = 'tyrant swain'
    if (augment_stats_units[i] == '_volibear'):
        augment_stats_units[i] = 'volibear'
    if (augment_stats_units[i][0:len(augment_stats_units[i])-2] == 'nomsy'):
        augment_stats_units[i] = 'nomsy'
    augment_stats_units[i] = re.sub(r'[^a-zA-Z]', '', augment_stats_units[i]).lower()

### get data for all units ###
driver.get('https://tactics.tools/units')
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')
    
# get all of the units' names
champ_name = []
for element in soup.findAll(attrs={'class': 'text-base font-medium whitespace-no-wrap truncate css-l6s31b'}):
    champ_name.append(re.sub(r'[^a-zA-Z]', '', element.text).lower())


# get the unit's playrate
champ_playrate = []
for element in soup.findAll(attrs={'class': 'w-[34px]'}):
    champ_playrate.append(re.sub(r'[^0-9.]', '', element.text))

# get the unit's average placement
champ_placement = []
for element in soup.findAll(attrs={'class': 'text-right css-wldxpd'}):
    champ_placement.append(re.sub(r'[^0-9.]', '', element.text))


conn_str = "mongodb+srv://colin:<password>@cluster0.zqayzpq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str)
db = client.tft

# this is super inefficent but I don't really want to think of another way since it works fine
count = 0
for i in range(len(augment_names)):
    augment_collection = {}
    augment_collection["augment"] = augment_names[i]
    augment_collection["placement"] = float(augment_stats_placement[i])
    augment_collection["top4%"] = float(augment_stats_top4[i])
    augment_collection["freqency"] = float(augment_stats_freq[i]) * 1000
    augment_collection["win%"] = float(augment_stats_win[i])
    temp_nestedDict = {}
    for i in range(3):
        temp_nestedDict["unit " + str(i)] = augment_stats_units[count]
        count += 1
    augment_collection["top units"] = temp_nestedDict
    db.augments.insert_one(augment_collection)

for i in range(len(champ_name)):
    unit_collection = {}
    unit_collection["unit"] = champ_name[i]
    unit_collection["placement"] = float(champ_placement[i])
    unit_collection["playrate"] = float(champ_playrate[i])
    db.units.insert_one(unit_collection)

# collection1 = db['augments']
# cursor = collection1.find({})
# for document in cursor:
#     print(document)

# collection1 = db['units']
# cursor = collection1.find({})
# for document in cursor:
#     print(document)