import json
from datetime import datetime


class manage:
    def start(rfid):
        with open('db.json', 'r') as openfile:  # open json file to store data
            json_object = json.load(openfile)
        if rfid in json_object.keys():
            data = manage.exit(rfid)
            data.append(manage.calculateCost(data))  # call function to calculate cost
            return data
        else:
            entryTime = manage.entry(rfid)
            return ['entry', entryTime]

    def exit(rfid):  # funtion store exit time
        exitTime = datetime.now()  # this method returns real time date and time
        with open('db.json', 'r') as openfile:
            json_object = json.load(openfile)

        eTime = json_object[rfid]
        entryTime = datetime.strptime(eTime, '%d/%m/%y %H:%M:%S')
        del json_object[rfid]

        # Serializing json
        json_object = json.dumps(json_object, indent=4)

        # Writing to sample.json
        with open("db.json", "w") as outfile:
            outfile.write(json_object)
        return ['exit', entryTime, exitTime]

    def entry(rfid):
        entryTime = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        print(type(entryTime))
        # Opening JSON file
        with open('db.json', 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
        json_object[rfid] = entryTime
        # Serializing json
        json_object = json.dumps(json_object, indent=4)

        # Writing to sample.json
        with open("db.json", "w") as outfile:
            outfile.write(json_object)
        etime = datetime.strptime(entryTime, '%d/%m/%y %H:%M:%S')
        return etime

    def calculateCost(data):
        rate = 10
        timeDiff = data[2] - data[1]
        minutes = timeDiff.total_seconds() / 60
        return minutes * rate
