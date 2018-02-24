import urllib2
import json
import base64
import sys

class WCap:
    def capture(self, url):
        api = "https://www.googleapis.com/pagespeedonline/v1/runPagespeed?screenshot=true&strategy=mobile&url=" + urllib2.quote(url)
        try:
            site_data = json.load(urllib2.urlopen(api))
            screenshot_encoded =  site_data['screenshot']['data']
            screenshot_encoded = screenshot_encoded.replace("_", "/")
            screenshot_encoded = screenshot_encoded.replace("-", "+")
            screenshot_decoded = base64.b64decode(screenshot_encoded)
            with open('screenshots/screenshot.jpg', 'wb') as file_:
                file_.write(screenshot_decoded)
        except:
            print "Screenshot Error"

WCap().capture("https://www.sfgate.com/politics/article/Trump-notecard-I-hear-you-Parkland-shooting-guns-12631457.php")
