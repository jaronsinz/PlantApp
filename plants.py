class Plant:
    name = ""
    height = 0
    lastTimeWatered = None

    def __init__(self, name, height, lastTimeWatered):
        self.name = name
        self.height = height
        self.lastTimeWatered = lastTimeWatered

class Task:
    dueTime: None
    plant: None

    def __init__(self, dueTime, plant):
        self.dueTime = dueTime
        self.plant = plant
