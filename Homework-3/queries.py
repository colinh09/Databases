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
print("Query 2: List augments that have an average placement below 4 and a top 4 percentage of above 60%.")
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

# these augments will be augments that are very niche/siutational, but strong in the right siutations
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

# this is a question that I would ask myself when trying to find good augments and what units would be good fit for it
print("Query 7: Get the units that best use the augment 'Better Together'. Average all the placement average of the augments and its top units.")

answer = db.augments.find({"augment": "Better Together"})

for i in answer:
    unit_list = i.get("top units")
    augment = i.get("placement")
print("The top units are: " + unit_list["unit 0"] + " " + unit_list["unit 1"] + " "  + unit_list["unit 2"])

answer2 = db.units.find({"unit": unit_list["unit 0"]})
answer3 = db.units.find({"unit": unit_list["unit 1"]})
answer4 = db.units.find({"unit": unit_list["unit 2"]})

for i in answer2:
    unit1 = i.get("placement")
for i in answer3:
    unit2 = i.get("placement")
for i in answer4:
    unit3 = i.get("placement")

average = (unit1 + unit2 + unit3 + augment) / 4
print("The average placement of the augment and its top units is: " + str(average))

