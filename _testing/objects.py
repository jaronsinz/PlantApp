import uuid

class Plant:
    id = None
    name = ""
    height = 0
    lastTimeWatered = None
    wateringCycleDays = 0

    def __init__(self, id, name, height, lastTimeWatered, wateringCycleDays):
        self.id = id
        self.name = name
        self.height = height
        self.lastTimeWatered = lastTimeWatered
        self.wateringCycleDays = wateringCycleDays

class Task:
    overdueTime: None
    plant: None

    def __init__(self, overdueTime, plant):
        self.overdueTime = overdueTime
        self.plant = plant

class User:
    id =  None
    name = ""
    plants = []

    def __init__(self, name):
        self.id = uuid.uuid1()
        self.name = name
