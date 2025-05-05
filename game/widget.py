from kivy.uix.widget import Widget
from kivy.clock import Clock
from asset_manager.manager import AssetManager
from .ui import setup_ui
from .audio import setup_audio
from .input_handler import setup_input


class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.asset_manager = AssetManager()
        self.current_sound = None  # Track the currently playing sound

        setup_ui(self)
        setup_audio(self)
        setup_input(self)

        # Update for smooth movement
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        pass

    def start_animation(self):
        from .animation import start_animation
        start_animation(self.char_image)
