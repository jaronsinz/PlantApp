from objects import Plant, Task, User
from datetime import datetime, timedelta
import json
from pathlib import Path
import uuid

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

myPlants = []
myTasks = []
jsonFilePath = "data/plants.json"

#reading and writing the data to a json file to save it between sessions

def readPlantsFromJson():
    print("loading...")
    with open(jsonFilePath, 'r') as openfile:
        plantsDict = json.load(openfile)
        if plantsDict:
            for plantDict in plantsDict.values():
                p1 = Plant(uuid.UUID(plantDict["id"]), plantDict["name"], plantDict["height"], datetime.strptime(plantDict["lastTimeWatered"], '%Y-%m-%dT%H:%M:%S.%f'), plantDict["wateringCycleDays"])
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
            "lastTimeWatered" : plant.lastTimeWatered,
            "wateringCycleDays" : plant.wateringCycleDays
        }
        plantsDict.update({f"Plant {plantNumber}":plantDict})

    with open(jsonFilePath, "w") as outfile:
        json.dump(plantsDict, outfile, default=json_serial)


#function that provides the current tasks

def calculateTasks(currentDate):
    myTasks.clear()
    for plant in myPlants:
        daysSinceWatering = currentDate - plant.lastTimeWatered
        overdueTime = daysSinceWatering - timedelta(days=plant.wateringCycleDays)

        if(overdueTime > timedelta(days=0)): 
            t1 = Task(overdueTime, plant)
            myTasks.append(t1)

#needs to be modified for GUI

def markTasksDone(currentDate):
    for task in myTasks:
        answer = input(f"Wurde {task.plant.name} gegossen? y/n\n")
        if(answer == "y"):
            myTasks.remove(task)
            task.plant.lastTimeWatered = currentDate
    ShowTasks.showTasks(currentDate)

#App 
class MenuButtons(GridLayout):
    pass

class MenuButton(Button):
    pass

class MenuBtnLabel(Label):
    pass

class MenuBtnImage(Image):
    pass
    

class AddPlant(Screen):
    #nameTextInput = ObjectProperty()
    #heightTextInput = ObjectProperty(None)
    #lTWTextInput = ObjectProperty(None)
    #plantInput = ObjectProperty(None)

    def addNewPlant(self):
        
        def calcWateringCycleDays():
            return 7
        
        name = self.nameTextInput.text
        height = self.heightTextInput.text
        currentDate = datetime.today()
        lastTimeWatered = currentDate - timedelta(days=int(self.lTWTextInput.text))
        wateringCycleDays = calcWateringCycleDays()

        p1 = Plant(uuid.uuid1(), name, height, lastTimeWatered, wateringCycleDays)
        myPlants.append(p1)

        savePlantsToJson() #unnötige Schreiblast, kann beschleunigt werden

class ShowTasks(Screen):
    buttons = ObjectProperty(None)
    tasksGrid = ObjectProperty(None)

    def on_enter(self):
        self.showTasks()

    def showTasks(self):
        calculateTasks(datetime.today())
        self.tasksGrid.clear_widgets()
        self.tasksGrid.rows = len(myTasks)

        for task in myTasks:
            taskRow = STRow()

            taskLabelPlantName = STLabel(text=task.plant.name, size_hint= (0.5, 1))
            taskLabelDueTime = STLabel(text=self.calcWateringInstant(task.overdueTime), size_hint= (0.5, 1))

            taskRow.add_widget(taskLabelPlantName)
            taskRow.add_widget(taskLabelDueTime)

            self.tasksGrid.add_widget(taskRow)

    def calcWateringInstant(self, overdueTime):
        if(overdueTime.days < 2):
            if(overdueTime.days < 1):
                return "Water Today!"
            else:
                return "Seit 1 Tag überfällig!"
        else:
            return f"Seit {overdueTime.days} Tagen  überfällig!"

class STRow(GridLayout):
    pass

class STLabel(Button):
    pass

class ShowPlants(Screen):
    plantsGrid = ObjectProperty(None)
    
    def on_enter(self):
        self.showPlants()

    def showPlants(self):
        self.plantsGrid.clear_widgets()
        self.plantsGrid.rows = len(myPlants)

        for plant in myPlants:
            plantRow = SPRow()

            plantLabel = SPLabel(text=plant.name)
            removeButton = SPRmvButton(rmvButtonID=plant.id, plantRow=plantRow)
            removeButton.bind(on_release = removeButton.deletePlant)

            plantRow.add_widget(plantLabel)
            plantRow.add_widget(removeButton)
            
            self.plantsGrid.add_widget(plantRow)
            

class SPRow(GridLayout):
    pass

class SPLabel(Button):
    pass

class SPRmvButton(Button):
    rmvButtonID = ObjectProperty()
    plantRow = ObjectProperty()

    def deletePlant(self, *args):
        for plant in myPlants:
            if (plant.id == self.rmvButtonID):
                myPlants.remove(plant)
        
        self.parent.parent.remove_widget(self.plantRow)
    
class WindowManager(ScreenManager):
    pass

class PlantApp(App):
    def build(self):
        kv = Builder.load_file("plantKV.kv")
        Window.bind(on_request_close=self.on_request_close)
        return kv
    
    def on_request_close(self, *args):
        savePlantsToJson()

    if Path(jsonFilePath).is_file():
        readPlantsFromJson()
    
if __name__ == "__main__":
    PlantApp().run()