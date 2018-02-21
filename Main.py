''' 
Primary class for setting up and controling screens

'''

from kivy.app import App
from kivy.app import Widget
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image, AsyncImage
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
from Settings import ifttt_settings 
from RedditParser import RParse
from WeatherParser import WParse
from AIOParser import AIOParse
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
        self.scheduleAio()
        self.size = (720, 480)
    
    def startIt(self, *args):
        self.current = "general"
    
    def scheduleAio(self, *args):
        enabled = App.get_running_app().config.get('IFTTT', 'aioEnabled')
        Clock.unschedule(self.pingAio)
        if enabled == "1":
            Clock.schedule_interval(self.pingAio, 10)

    def pingAio(self, *args):
        aioUsername = App.get_running_app().config.get('IFTTT', 'aioUsername')
        aioKey = App.get_running_app().config.get('IFTTT', 'aioKey')
        aioFeed = App.get_running_app().config.get('IFTTT', 'aioFeedKey')
        if aioUsername != "" and aioKey != "" and aioFeed != "":
            data = AIOParse().getLastItem(aioUsername, aioFeed, aioKey)
            if len(data) > 0:
                self.handleRequest(data)
        
    def handleRequest(self, data):
        if data[0] == "info":
            self.get_screen("aio").set_color(data[1])
            self.get_screen("aio").set_text(data[2])
            if len(data) > 3:
                self.get_screen("aio").set_title(data[3])
            if len(data) > 5:
                self.get_screen("aio").set_image(data[4]+":"+data[5])
            prevTransition = self.transition
            self.transition = RiseInTransition()
            self.current = "aio"
            self.transition = prevTransition

class AIOScreen(Screen):
    title = StringProperty("")
    header = StringProperty("")
    subtext = StringProperty("")
    imageSource = StringProperty("")
    color = ListProperty([0,0,0,0.5])
    def __init__(self, **kwargs):
        super(AIOScreen, self).__init__(**kwargs)

    def set_title(self, title):
        self.title = title
    
    def set_image(self, image):
        self.imageSource = image

    def set_color(self, color):
        rgba = color.split(",")
        if len(rgba) == 4:
            self.color = [int(rgba[0])/255.0,int(rgba[1])/255.0,int(rgba[2])/255.0,int(rgba[3])/255.0]

    def set_text(self, data):
        parts = data.split(",")
        self.header = parts[0]
        self.subtext = parts[1]

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
        enabled = App.get_running_app().config.get('RedditRising', 'rrenabled')
        if enabled == "1":
            posts = RParse().getRisingNews(subs, int(minups))
            for post in posts:
                title = post[0]
                color = [0,0,0,0.4]
                if post[4] == 1 or post[4] == "1" or post[5] == True or post[5] == "True":
                    color = [1,0,0,0.4]
                title = '\n'.join(title[i:i+26] for i in range(0, len(title), 26))
                if(len(title) > 64):
                    title = title[:64]+"..."
                self.children[0].add_widget(RedditLink(text=title, thumbnail=post[2], ups=str(post[3]), source=post[6], color=color, url=post[2]))

class RedditLink(Widget):
    text = StringProperty("Text Not Set")
    thumbnail = StringProperty("icons/reddit.png")
    ups = StringProperty("----")
    source = StringProperty("unknown")
    color = ListProperty([0,0,0,0.4])
    url = StringProperty("")
    def __init__(self, **kwargs):
        super(RedditLink, self).__init__(**kwargs)
        self.size = (280, 70)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            view = ModalView(size_hint=(None, None), size=(600,400))
            #view.add_widget(RedditLink(text=self.text,thumbnail=self.thumbnail,ups=self.ups,source=self.source,color=self.color))
            view.add_widget(AsyncImage(source=self.url))
            view.open()

class WeatherBox(Widget):
    def __init__(self, **kwargs):
        super(WeatherBox, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        apiKey = App.get_running_app().config.get('Weather', 'wuKey')
        zipCode = App.get_running_app().config.get('Weather', 'zip')
        if self.collide_point(touch.x, touch.y):
            view = ModalView(size_hint=(None, None), size=(600,400))
            if apiKey != "":
                image = WParse().getForecastMap(apiKey, zipCode)
                view.add_widget(AsyncImage(source=image,halign='middle'))
            else:
                view.add_widget(Label(text="Uhohs: No API Key Set\nUpdate Weather Underground API Key in Settings"))
            view.open()

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
                'rrenabled': True
            } 
        )
        config.setdefaults('Weather',
            {
                'zip': '20001',
                'owmKey': '',
                'wuKey': '',
            } 
        )
        config.setdefaults('IFTTT',
            {
                'aioKey': '',
                'aioEnabled': False,
                'aioUsername': '',
                'aioFeedKey': ''
            } 
        )
    
    def build_settings(self, settings): 
        settings.add_json_panel('General', self.config, data=general_settings)
        settings.add_json_panel('Weather', self.config, data=weather_settings)
        settings.add_json_panel('IFTTT', self.config, data=ifttt_settings)

    def on_config_change(self, config, section, key, value):
        if key == "wallpaperSourceOne" or key == "wallpaperSourceTwo" or key == "wallpaperRefresh":
            self.main.change_bg()

if __name__ == '__main__':
    #Builder.load_file("PiHome.kv")
    Window.size = (800,480)
    #Window.fullscreen = True
    PiHomeApp().run()