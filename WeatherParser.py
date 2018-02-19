import requests
import json

class WParse:

    def getCurrentWeather(self, key, zip):
        url = 'http://api.openweathermap.org/data/2.5/weather?zip='+zip+',us&units=imperial&appid='+key
        r = requests.get(url)
        data = json.loads(r.text)
        city = data['name']
        weather = data['weather'][0]['main']
        temp  = data['main']['temp']
        return [city, weather, temp]


#WParse().getCurrentWeather() 