''' 
Primary class for setting up and controling screens

'''

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.animation import Animation
from kivy.animation import AnimationTransition


class GeneralScreen(Screen):
    
    pass

class WeatherScreen(Screen):
    pass


manager = ScreenManager()
manager.add_widget(GeneralScreen(name='general'))
manager.add_widget(WeatherScreen(name='weather'))

class  PiHomeApp(App):
    def build(self):
        return manager


if __name__ == '__main__':
    PiHomeApp().run()