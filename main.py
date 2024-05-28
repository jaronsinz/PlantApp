from objects import Plant, Task, User
from datetime import datetime, timedelta
import json
from pathlib import Path
import uuid

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window

myPlants = []
myTasks = []
jsonFilePath = "data/plants.json"
daysBetweenWatering = 7

#reading and writing the data to a json file to save it between sessions

def readPlantsFromJson():
    print("loading...")
    with open(jsonFilePath, 'r') as openfile:
        plantsDict = json.load(openfile)
        if plantsDict:
            for plantDict in plantsDict.values():
                p1 = Plant(uuid.UUID(plantDict["id"]), plantDict["name"], plantDict["height"], datetime.strptime(plantDict["lastTimeWatered"], '%Y-%m-%dT%H:%M:%S.%f'))
                myPlants.append(p1)

def json_serial(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    
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


#function that provides the current tasks

def calculateTasks(currentDate):
    myTasks.clear()
    for plant in myPlants:
        daysSinceWatering = currentDate - plant.lastTimeWatered
        if(daysSinceWatering > timedelta(days=daysBetweenWatering)):
            dueTime = currentDate - (daysSinceWatering - timedelta(days=7))
            t1 = Task(dueTime, plant)
            myTasks.append(t1)

#needs to be modified for GUI

def markTasksDone(currentDate):
    for task in myTasks:
        answer = input(f"Wurde {task.plant.name} gegossen? y/n\n")
        if(answer == "y"):
            myTasks.remove(task)
            task.plant.lastTimeWatered = currentDate
    MainGrid.showTasks(currentDate)

#App 

class MainGrid(Widget):
    outputLabel = ObjectProperty(None)
    nameTextInput = ObjectProperty(None)
    heightTextInput = ObjectProperty(None)
    lTWTextInput = ObjectProperty(None)

    def addNewPlant(self):
        name = self.nameTextInput.text
        height = self.heightTextInput.text
        currentDate = datetime.today()
        lastTimeWatered = currentDate - timedelta(days=int(self.lTWTextInput.text))

        p1 = Plant(uuid.uuid1(), name, height, lastTimeWatered)
        myPlants.append(p1)
        self.outputLabel.text = f"{p1.name} was added to ur plants"
        savePlantsToJson() #unnötige Schreiblast, kann beschleunigt werden

    def showTasks(self):
        calculateTasks(datetime.today())
        tasks_str = ""
        for task in myTasks:
            tasks_str += f"{task.plant.name} muss gegossen werden! Fällig: {task.dueTime.date()}\n"
        self.outputLabel.text = tasks_str

class PlantApp(App):
    def build(self):
        Window.bind(on_request_close=self.on_request_close)
        return MainGrid()
    
    def on_request_close(self, *args):
        savePlantsToJson()

    if Path(jsonFilePath).is_file():
        readPlantsFromJson()
    
if __name__ == "__main__":
    PlantApp().run()