import json

with open('upstage_test.json', "r") as json_file:
    data = json.load(json_file)
    data = data['elements'][0]
    print(data)
