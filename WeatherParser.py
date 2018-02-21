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

    def getForecast(self, key, zip, days): 
        url = 'http://api.openweathermap.org/data/2.5/forecast?zip='+zip+',us&units=imperial&appid='+key
        r = requests.get(url)
        data = json.loads(r.text)
        forecast = []
        for x in range(0, days):
            today = data['list'][x*8]
            day = [today['weather'][0]['main'],today['weather'][0]['icon'],int(round(today['main']['temp']))]
            forecast.append(day)
        return forecast

    def getForecastMap(self, key, zip):
        return "http://api.wunderground.com/api/"+key+"/animatedradar/q/zip/"+zip+"/image.gif?width=600&height=400&newmaps=1&noclutter=1"

#WParse().getCurrentWeather() 