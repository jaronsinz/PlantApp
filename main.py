from objects import Plant, Task
from datetime import datetime, timedelta
import json
from pathlib import Path
import uuid

myPlants = []
myTasks = []
jsonFilePath = "data/plants.json"
daysBetweenWatering = 7

def main():
    if Path(jsonFilePath).is_file():
        readPlantsFromJson()
    else:
        checkIfNewPlant()

def readPlantsFromJson():
    with open(jsonFilePath, 'r') as openfile:
        plantsDict = json.load(openfile)
        if plantsDict:
            for plantDict in plantsDict.values():
                p1 = Plant(uuid.UUID(plantDict["id"]), plantDict["name"], plantDict["height"], datetime.strptime(plantDict["lastTimeWatered"], '%Y-%m-%dT%H:%M:%S.%f'))
                myPlants.append(p1)
    checkIfNewPlant()

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()

def addNewPlant():
    name = input("Name of Plant: ")
    height = int(input("Height of Plant (cm): "))
    currentDate = datetime.today()
    lastTimeWatered = currentDate - timedelta(days=int(input("How many days ago was your plant watered?: ")))

    p1 = Plant(name, height, lastTimeWatered)
    myPlants.append(p1)
    savePlantsToJson() #unnötige Schreiblast, kann beschleunigt werden
    checkIfNewPlant()

def calculateTasks(currentDate):
    myTasks.clear()
    for plant in myPlants:
        daysSinceWatering = currentDate - plant.lastTimeWatered
        if(daysSinceWatering > timedelta(days=daysBetweenWatering)):
            dueTime = currentDate - (daysSinceWatering - timedelta(days=7))
            t1 = Task(dueTime, plant)
            myTasks.append(t1)

def markTasksDone(currentDate):
    for task in myTasks:
        answer = input(f"Wurde {task.plant.name} gegossen? y/n\n")
        if(answer == "y"):
            myTasks.remove(task)
            task.plant.lastTimeWatered = currentDate
    showTasks(currentDate)

def checkIfMarkTasksDone(currentDate):
    answer = input("Aufgaben als erledigt markieren? y/n\n")
    if(answer == "y"):
        markTasksDone(currentDate)
    else:
        checkIfNewPlant()

def showTasks(currentDate):
    for task in myTasks:
        print(f"{task.plant.name} muss gegossen werden! Fällig: {task.dueTime.date()}")
    checkIfMarkTasksDone(currentDate)

def checkIfShowTasks():
    answer = input("Anstehende Aufgaben anzeigen? y/n\n")
    if(answer == "y"):
        currentDate = datetime.today()
        calculateTasks(currentDate)
        showTasks(currentDate)
    else:
        checkIfNewPlant()

def checkIfNewPlant():
    answer = input("Neue Pflanze hinzufügen? y/n\n")
    if(answer == "y"):
        addNewPlant()
    else:
        checkIfShowTasks()

def savePlantsToJson():
    print("saving...")
    plantsDict = {}
    for plantNumber, plant in enumerate(myPlants):
        plantDict = {
            "id" : str(plant.id),
            "name" : plant.name,
            "height" : plant.height,
            "lastTimeWatered" : plant.lastTimeWatered
        }
        plantsDict.update({f"Plant {plantNumber}":plantDict})

    with open(jsonFilePath, "w") as outfile:
        json.dump(plantsDict, outfile, default=json_serial)

main()