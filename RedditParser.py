import json
import requests
import random
import urllib
from random import randint
import os, glob
import uuid

class RParse:
    count = 0
    def selectRandomUrl(self, subreddit):
        r = requests.get('https://www.reddit.com/r/'+subreddit+'/.json', headers = {'User-agent': 'Chrome'})
        data = json.loads(r.text)
        posts = data['data']['children']
        filename = "default_bg.jpg"
        success = False
        self.count = 0
        for f in glob.glob("wallpapers/dbg_*"):
            os.remove(f)
        while success == False and self.count < 5:
            try:
                url = ""
                while not (url.endswith(".jpg")):
                    post = posts[randint(0, 25)]['data']
                    url = post['url']
                hsh = uuid.uuid4().hex[:8]
                filename = "wallpapers/dbg_"+hsh+"."+url[-3:]
                urllib.urlretrieve(url, filename)
                success = True
            except:
                self.count = self.count + 1
                filename = "default_bg.jpg"
                print "Failed to update"
        return filename

    def getRisingNews(self, subreddit, minUps):
        r = requests.get('https://www.reddit.com/r/'+subreddit+'/rising/.json', headers = {'User-agent': 'Chrome'})
        data = json.loads(r.text)
        posts = data['data']['children']
        current = []
        for post in posts:
            title =  post['data']['title']
            url =  post['data']['url']
            thumbnail = post['data']['thumbnail']
            ups = post['data']['ups']
            gold = post['data']['gilded']
            pinned = post['data']['pinned']
            source = post['data']['domain']
            
            if ups >= minUps or gold == "1" or gold == 1 or pinned == True or pinned == "True":
                current.append([title,url,thumbnail,ups,gold,pinned,source])

        return current
