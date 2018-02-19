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


#WParse().getCurrentWeather() 