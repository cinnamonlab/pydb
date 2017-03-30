import json


class JsonLoader:
    # write json loader functions here and decode json to object too
    def loadIntent(self, jsonfile):
        with open(jsonfile) as datafile:
            data = json.load(datafile)
        return data

    def loadBotConfig(self, jsonfile):
        with open(jsonfile) as datafile:
            data = json.load(datafile)
        return data
