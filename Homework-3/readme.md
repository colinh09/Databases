# Problem Set 3: Webscraper
This assignment has two files written in python: scraper.py and db.py.

Scraper.py will scrape data from a website called tactics.tools: https://tactics.tools/

I realize that when you look at the website, you likely will not understand a single thing that is going on. Tactics.tools is a stat based website for a game called teamfight tactics, which is an autobattler game that is a spin off of league of legends (the characters) and Dota Auto Chess (the gameplay). In the game, you can upgrade and buy "units" that will build up your team. You can also select "augments" that will either enhance your economy or the overall combat power of your team. Each augment and unit will have different statistics attached to them, one of which is placement average. There are 8 players, so your placement can range from 1 to 8.

The scraper will create a selenium chrome driver to allow the beautiful soup library to parse the HTML on the page for the desired data. The desired data will the placement average / top 4 placement percentage for augments and units: https://tactics.tools/augments, https://tactics.tools/units. I will then store the collected data within a MongoDB database.

In the db.py file, I will query the database on various things relating to the average placement of the augments and items. 
