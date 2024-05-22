import json
outerDict = {}
innerDict = {}

for i in range(5):
    innerDict = {
        "name" : f"Meine Pflanze {i}",
        "height" : 20
    }
    outerDict.update({f"Plant {i}":innerDict})

with open("test.json", "w") as outfile:
    json.dump(outerDict, outfile)
    