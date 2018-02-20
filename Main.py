''' 
Primary class for setting up and controling screens

'''

from kivy.app import App
from kivy.app import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.animation import AnimationTransition, Animation
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import SettingsWithSidebar
from kivy.properties import StringProperty
from kivy.properties import ListProperty 
from Settings import general_settings 
from Settings import weather_settings 
from RedditParser import RParse
from WeatherParser import WParse
import time

class MainContainer(FloatLayout):
    def __init__(self, **kwargs):
        super(MainContainer, self).__init__(**kwargs)
        Clock.schedule_once(self.change_bg, 5)
        Clock.schedule_interval(self.change_bg, 60)
        with self.canvas.before:
            self.bg = Rectangle(source="default_bg.jpg", pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)


    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def change_bg(self, *args):
        enabled = App.get_running_app().config.get('General', 'wallpaperRefresh')
        if enabled == "1":
            source = App.get_running_app().config.get('General', 'wallpaperSourceOne')
            name = RParse().selectRandomUrl(source)
            try:
                self.bg.source = name
            except:
                self.bg.source = "default_bg.jpg"
        else:
            self.bg.source = "default_bg.jpg"

class SnackBar(FloatLayout):
    def __init__(self, **kwargs):
        super(SnackBar, self).__init__(**kwargs)
        self.size = (80, 480)
        with self.canvas:
            Color(0,0,0,0.2)
            Rectangle(pos=(0,0), size=self.size)

class SnackBarButton(Button):
    def __init__(self, **kwargs):
        super(SnackBarButton, self).__init__(**kwargs)
        self.background_color = [0,0,0,0]

class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        Clock.schedule_once(self.startIt, 5)
        self.size = (720, 480)
    
    def startIt(self, *args):
        self.current = "general"

class GeneralScreen(Screen):
    def __init__(self, **kwargs):
        super(GeneralScreen, self).__init__(**kwargs)
        self.size = (720, 480)
        Clock.schedule_interval(self.update, 1)
        Clock.schedule_once(self.update_weather, 2)
        Clock.schedule_interval(self.update_weather, 600)
        with self.canvas:
            Color(240,240,0,0.0)
            Rectangle(pos=(0,0), size=self.size)
            
    def update(self, *args):
        clock = self.ids.gclock
        date = self.ids.gdate
        clock.text = time.strftime( "%I:%M %p")
        date.text = time.strftime("%A %B %d, %Y")

    def update_weather(self, *args):
        apiKey = App.get_running_app().config.get('Weather', 'owmKey')
        zipCode = App.get_running_app().config.get('Weather', 'zip')
        weather = self.ids.gweather 
        temp = self.ids.gtemp 
        if apiKey != "":
            weatherData = WParse().getCurrentWeather(apiKey, zipCode)
            weather.text = weatherData[0] + " | " + weatherData[1]
            temp.text = str(weatherData[2]) +u'\xb0'+ "F"
        else:
            weather.text = "No API Key Set" 
            temp.text = "--"+u'\xb0'+"F"


class WeatherScreen(Screen):
    def __init__(self, **kwargs):
        super(WeatherScreen, self).__init__(**kwargs)
        self.size = (720, 480)
        with self.canvas:
            Color(240,240,240,0.0)
            Rectangle(pos=(0,0), size=self.size)

    def loadWeather(self, *args):
        apiKey = App.get_running_app().config.get('Weather', 'owmKey')
        zipCode = App.get_running_app().config.get('Weather', 'zip')
        today = self.ids.today
        tomorrow = self.ids.tomorrow
        nextDay = self.ids.nextDay
        if apiKey != "":
            weatherData = WParse().getForecast(apiKey, zipCode, 3)
            today.forecast = weatherData[0][0]
            today.imgSource = weatherData[0][1]+".png"
            today.temp = str(weatherData[0][2])+u'\xb0'+"F"

            tomorrow.forecast = weatherData[1][0]
            tomorrow.imgSource = weatherData[1][1]+".png"
            tomorrow.temp = str(weatherData[1][2])+u'\xb0'+"F"

            nextDay.forecast = weatherData[2][0]
            nextDay.imgSource = weatherData[2][1]+".png"
            nextDay.temp = str(weatherData[2][2])+u'\xb0'+"F"


class HomeControlScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeControlScreen, self).__init__(**kwargs)
        self.size = (720, 480)
        with self.canvas:
            Color(0,0,0,0.5)
            Rectangle(pos=(0,0), size=self.size)

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        self.size = (720, 480)
        with self.canvas:
            Color(0,0,0,0.2)
            Rectangle(pos=(0,0), size=self.size)


class RedditRising(ScrollView):
    def __init__(self, **kwargs):
        super(RedditRising, self).__init__(**kwargs)
        Clock.schedule_once(self.update_links, 8)
        Clock.schedule_interval(self.update_links, 300)

    def update_links(self, *args):
        self.children[0].clear_widgets()
        subs = App.get_running_app().config.get('RedditRising', 'rrsource')
        minups = App.get_running_app().config.get('RedditRising', 'rrups')
        posts = RParse().getRisingNews(subs, int(minups))
        for post in posts:
            title = post[0]
            color = [0,0,0,0.4]
            if post[4] == 1 or post[4] == "1" or post[5] == True or post[5] == "True":
                color = [1,0,0,0.4]
            title = '\n'.join(title[i:i+26] for i in range(0, len(title), 26))
            if(len(title) > 64):
                title = title[:64]+"..."
            self.children[0].add_widget(RedditLink(text=title, thumbnail=post[2], ups=str(post[3]), source=post[6], color=color))

class RedditLink(Widget):
    text = StringProperty("Text Not Set")
    thumbnail = StringProperty("icons/reddit.png")
    ups = StringProperty("----")
    source = StringProperty("unknown")
    color = ListProperty([0,0,0,0.4])
    def __init__(self, **kwargs):
        super(RedditLink, self).__init__(**kwargs)
        self.size = (280, 70)

class WeatherBox(Widget):
    pass

class  PiHomeApp(App):
    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        mc = MainContainer()
        self.main = mc
        return mc
    
    def build_config(self, config):
        config.setdefaults('General',
            {
                'wallpaperRefresh': True,
                'wallpaperSourceOne': 'wallpapers+earthporn',
                'wallpaperSourceTwo': '',
                'wallpaperActiveSource': 'Source One',
            } 
        )
        config.setdefaults('RedditRising',
            {
                'rrsource': 'politics',
                'rrups': 350,
            } 
        )
        config.setdefaults('Weather',
            {
                'zip': '20001',
                'owmKey': '',
            } 
        )
    
    def build_settings(self, settings): 
        settings.add_json_panel('General', self.config, data=general_settings)
        settings.add_json_panel('Weather', self.config, data=weather_settings)

    def on_config_change(self, config, section, key, value):
        if key == "wallpaperSourceOne" or key == "wallpaperSourceTwo" or key == "wallpaperRefresh":
            self.main.change_bg()

if __name__ == '__main__':
    #Builder.load_file("PiHome.kv")
    Window.size = (800,480)
    #Window.fullscreen = True
    PiHomeApp().run()