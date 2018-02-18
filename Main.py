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
from kivy.animation import AnimationTransition, Animation
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.uix.scrollview import ScrollView
from kivy.uix.settings import SettingsWithSidebar
from kivy.properties import StringProperty
from Settings import general_settings 
from RedditParser import RParse
import time

class MainContainer(FloatLayout):
    def __init__(self, **kwargs):
        super(MainContainer, self).__init__(**kwargs)
        Clock.schedule_once(self.change_bg, 2)
        Clock.schedule_interval(self.change_bg, 10)
        with self.canvas.before:
            self.bg = Rectangle(source="default_bg.jpg", pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def change_bg(self, *args):
        source = App.get_running_app().config.get('General', 'wallpaperSourceOne')
        name = RParse().selectRandomUrl(source)
        self.bg.source = name
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
        with self.canvas:
            Color(240,240,0,0.0)
            Rectangle(pos=(0,0), size=self.size)
            
    def update(self, *args):
        clock = self.ids.gclock
        clock.text = time.strftime( "%I:%M %p")

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
            Color(240,240,240,0.8)
            Rectangle(pos=(0,0), size=self.size)

class RedditRising(ScrollView):
    def __init__(self, **kwargs):
        super(RedditRising, self).__init__(**kwargs)
#       with self.canvas:
#           Color(0,1,0,1)
#           Rectangle(pos=(0,0), size=self.size)


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
    
    def build_settings(self, settings): 
        settings.add_json_panel('General', self.config, data=general_settings)

    def on_config_change(self, config, section, key, value):
        self.main.change_bg()

if __name__ == '__main__':
    #Builder.load_file("PiHome.kv")
    Window.size = (800,480)
    #Window.fullscreen = True
    PiHomeApp().run()