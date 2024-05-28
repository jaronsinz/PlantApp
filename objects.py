import uuid

class Plant:
    id = None
    name = ""
    height = 0
    lastTimeWatered = None

    def __init__(self, name, height, lastTimeWatered):
        self.id = uuid.uuid1()
        self.name = name
        self.height = height
        self.lastTimeWatered = lastTimeWatered

class Task:
    dueTime: None
    plant: None

    def __init__(self, dueTime, plant):
        self.dueTime = dueTime
        self.plant = plant

class User:
    id =  None
    name = ""
    plants = []

    def __init__(self, name):
        self.id = uuid.uuid1()
        self.name = name
