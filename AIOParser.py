import json
import requests
import random
import urllib
from random import randint
import os, glob
import uuid

class AIOParse:
    def getLastItem(self, aioUser, aioFeed, apikey):
        last = ""
        try:
            url = "https://io.adafruit.com/api/v2/"+aioUser+"/feeds/"+aioFeed+"/data/last"
            r = requests.get(url, headers = {'X-AIO-Key': apikey})
            data = json.loads(r.text)

            if 'value' in data:
                itemId = data['id']
                self.deleteItem(aioUser, aioFeed, apikey, itemId)
                # Format key:rgba color:data_string
                last = data['value'].split(";")
        except Exception as E:
            print E
            last = ""
        return last

    def deleteItem(self, aioUser, aioFeed, apikey, itemId):
        try:
            url = "https://io.adafruit.com/api/v2/"+aioUser+"/feeds/"+aioFeed+"/data/"+itemId
            r = requests.delete(url, headers = {'X-AIO-Key': apikey})
        except:
            last = ""


#AIOParse().getLastItem("byakko00", "pihome","4db30b7befc340a88f50e51f89809b30")
#AIOParse().deleteItem("byakko00", "pihome","4db30b7befc340a88f50e51f89809b30", "0DT4E6M679VW14VQ4WSKPZJ0FT")