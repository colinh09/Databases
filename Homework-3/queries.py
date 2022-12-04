import pymongo
from pymongo import MongoClient

conn_str = "mongodb+srv://colin:<password>@cluster0.zqayzpq.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(conn_str)
db = client.tft

# this will list the "worst" unit
print("Query 1: What unit has the highest average placement and what was its placement?")
answer = db.units.find_one(sort=[("placement", pymongo.DESCENDING)])
print("The unit with the highest average placement is " + str(answer["unit"]) + " with an average placement of " + str(answer["placement"]) + "\n")

# this will list really good augments
print("Query 2: List augments that have an average placement below 4.5 and a top 4 percentage of above 50%.")
answer = db.augments.find({"placement": {"$lt": 4}, "top4%": {"$gt": 60}})
for i in answer:
    print(i.get("augment"))
print("\n")

# this will list terrible augments
print("Query 3: List the augments with an average placement above 5.")
answer = db.augments.find({"placement": {"$gt": 5}})
for i in answer:
    print(i.get("augment"))
print("\n")

# this will list units that are not contested, but are also strong
print("Query 4: List the 10 least frequently used units. Of that list, find the unit with the lowest average placement.")

answer = db.units.aggregate([
    {
        "$sort": { "playrate": 1 }
    },
    { "$limit": 10},
    {
        "$sort": { "placement": 1 }
    },
    {"$limit": 1}
])
for i in answer:
    print(i.get("unit"))
print("\n")


# just get the highest picked augment and how many times it has been picked
print("Query 5: List the augment with the highest pick rate. Print out how many times it has been picked.")
answer = db.augments.aggregate([
    {
        "$sort": { "freqency": -1 }
    },
    { "$limit": 1},
])
for i in answer:
    print(i.get("augment") + " has been chosen " + str(int(i.get("freqency"))) + " times.")
print("\n")

# the same as query 6 but in augment form
print("Query 6: Pick the 20 least frequently used augments. Of that list, find the top 5 augments with the highest win rate.")

answer = db.augments.aggregate([
    {
        "$sort": { "freqency": 1 }
    },
    {"$limit": 20},
    {
        "$sort": { "win%": -1 }
    },
    {"$limit": 5}
])

for i in answer:
    print(i.get("augment"))
print("\n")
