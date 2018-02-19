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
            self.bg = Rectangle(source="default_bg_2.jpg", pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)


    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def change_bg(self, *args):
        source = App.get_running_app().config.get('General', 'wallpaperSourceOne')
        name = RParse().selectRandomUrl(source)
        try:
            self.bg.source = name
        except:
            self.bg.source = "default_bg_2.jpg"
        self.bg.pos = self.pos
        self.bg.size = self.size

class SnackBar(FloatLayout):
    def __init__(self, **kwargs):
        super(SnackBar, self).__init__(**kwargs)
        self.size = (80, 480)
        with self.canvas:
            Color(200,200,200,0.1)
            Rectangle(pos=(0,0), size=self.size)

class SnackBarButton(Button):
    def __init__(self, **kwargs):
        super(SnackBarButton, self).__init__(**kwargs)
        self.background_color = [0,0,0,0]

class Manager(ScreenManager):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.size = (720, 480)

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
            temp.text = str(weatherData[2]) + "F"
        else:
            weather.text = "No API Key Set" 
            temp.text = "--F"


class WeatherScreen(Screen):
    def __init__(self, **kwargs):
        super(WeatherScreen, self).__init__(**kwargs)
        self.size = (720, 480)
        with self.canvas:
            Color(240,240,240,0.2)
            Rectangle(pos=(0,0), size=self.size)

class HomeControlScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeControlScreen, self).__init__(**kwargs)
        self.size = (720, 480)
        with self.canvas:
            Color(0,0,0,0.5)
            Rectangle(pos=(0,0), size=self.size)

class RedditRising(ScrollView):
    def __init__(self, **kwargs):
        super(RedditRising, self).__init__(**kwargs)
        #Clock.schedule_interval(self.update_links, 5)
#       with self.canvas:
#           Color(0,1,0,1)
#           Rectangle(pos=(0,0), size=self.size)

    def update_links(self, *args):
        self.children[0].clear_widgets()
        self.children[0].add_widget(RedditLink())
        self.children[0].add_widget(RedditLink())

class RedditLink(Widget):
    def __init__(self, **kwargs):
        super(RedditLink, self).__init__(**kwargs)
        self.size = (280, 70)
        with self.canvas.before:
            Color(0,0,0,0.4)
            Rectangle(pos=(0,0), size=self.size)



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
        self.main.change_bg()

if __name__ == '__main__':
    #Builder.load_file("PiHome.kv")
    Window.size = (800,480)
    #Window.fullscreen = True
    PiHomeApp().run()