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
        filename = "default_bg_2.jpg"
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
                filename = "default_bg_2.jpg"
                print "Failed to update"
        return filename

