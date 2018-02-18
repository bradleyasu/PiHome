import json
import requests
import random
import urllib
from random import randint
import os, glob

class RParse:
    count = 0
    def selectRandomUrl(self, subreddit):
        r = requests.get('https://www.reddit.com/r/'+subreddit+'/.json', headers = {'User-agent': 'Chrome'})
        data = json.loads(r.text)
        posts = data['data']['children']
        filename = "default_bg.jpg"
        success = False
        self.count = 0
        while success == False and self.count < 5:
            try:
                url = ""
                while not (url.endswith(".jpg") or url.endswith(".png")):
                    post = posts[randint(0, 25)]['data']
                    url = post['url']

                for f in glob.glob("wallpapers/dbg_*"):
                    os.remove(f)

                filename = "wallpapers/dbg_"+url.split("/")[-1] 
                urllib.urlretrieve(url, filename)
                success = True
            except:
                self.count = self.count + 1
                filename = "default_bg.jpg"
                print "Failed to update"
        return filename

