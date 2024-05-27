import json
from datetime import datetime, timedelta
from objects import Plant
jsonFilePath = "data/plants.json"

myPlants = []
today = datetime.today()
testPlant1 = Plant("Kaktus", 20, today)
testPlant2 = Plant("Einblatt", 40, today)
testPlant3 = Plant("Orchidee", 60, today)

myPlants.append(testPlant1)
myPlants.append(testPlant2)
myPlants.append(testPlant3)

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    
def savePlantsToJson():
    plantsDict = {}
    for plantNumber, plant in enumerate(myPlants):
        plantDict = {
            "name" : plant.name,
            "height" : plant.height,
            "lastTimeWatered" : plant.lastTimeWatered
        }
        plantsDict.update({f"Plant {plantNumber}":plantDict})

    with open(jsonFilePath, "w") as outfile:
        json.dump(plantsDict, outfile, default=json_serial)

savePlantsToJson()

myPlants = []
with open(jsonFilePath, 'r') as openfile:
    plantsDict = json.load(openfile)
    if plantsDict:
        for plantDict in plantsDict.values():
            readPlant = Plant(plantDict["name"], plantDict["height"], datetime.strptime(plantDict["lastTimeWatered"], '%Y-%m-%dT%H:%M:%S.%f'))
            myPlants.append(readPlant)

daysSinceWatering = today - myPlants[1].lastTimeWatered - timedelta(days=1)
print(daysSinceWatering)
