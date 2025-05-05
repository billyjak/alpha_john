from kivy.app import App
from kivy.core.window import Window
from .widget import GameWidget


class GameApp(App):
    def build(self):
        Window.fullscreen = False
        Window.size = (1280, 720)
        return GameWidget()
