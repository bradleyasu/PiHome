''' 
Primary class for setting up and controling screens

'''

from kivy.app import App
from kivy.app import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.animation import AnimationTransition, Animation
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from kivy.uix.scrollview import ScrollView

class MainContainer(FloatLayout):
    def __init__(self, **kwargs):
        super(MainContainer, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source="default_bg.jpg", pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)

    def update_bg(self, *args):
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
        with self.canvas:
            Color(240,240,240,0.0)
            Rectangle(pos=(0,0), size=self.size)
            

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
        return MainContainer()


if __name__ == '__main__':
    Window.size = (800,480)
    #Window.fullscreen = True
    PiHomeApp().run()