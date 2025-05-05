import os
from kivy.animation import Animation
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (1280, 720)

        self.asset_manager = AssetManager()
        self.current_sound = None  # Track the currently playing sound

        load_background_image(self)
        load_background_music(self)
        add_image_widget(self)

        # Bind keyboard input
        Window.bind(on_key_down=self.on_keystroke_down)
        # Update for smooth movement
        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def on_keystroke_down(self, window, key, scancode, codepoint, modifier):
        shifted_numbers_map = {
            "0": "close_paren", "1": "exclamation_mark", "2": "at", "3": "pound_sign",
            "4": "dollar_sign", "5": "percent", "6": "carat", "7": "ampersand",
            "8": "asterisk", "9": "open_paren"
        }
        shifted_symbols_map = {
            "]": "close_curly_brace", ";": "colon", "'": "double_quote",
            ",": "left_angle_bracket", "[": "open_curly_brace", "\\": "pipe",
            "=": "plus", "/": "question_mark", ".": "right_angle_bracket",
            "`": "tilde", "-": "underscore"
        }
        symbols_map = {
            "\\": "backslash", "`": "backtick", "]": "close_square_bracket",
            ",": "comma", "=": "equals", "-": "minus", "[": "open_square_bracket",
            ".": "period", ";": "semicolon", "'": "single_quote", "/": "slash"
        }

        is_shift = 'shift' in modifier
        char = None

        if codepoint and codepoint.isalpha():
            char = codepoint.upper() if is_shift else codepoint
        elif codepoint and codepoint.isdigit():
            char = shifted_numbers_map.get(codepoint) if is_shift else codepoint
        elif codepoint:
            char = shifted_symbols_map.get(codepoint) if is_shift else symbols_map.get(codepoint)

        if not char:
            return True

        # Update the single character image
        img_path = self.asset_manager.images.get(char)
        if img_path:
            self.char_image.source = img_path  # Replace the image
            # Cancel any running animation
            if self.char_image.current_anim:
                self.char_image.current_anim.cancel(self.char_image)
            self.start_animation()
        else:
            return True

        self.play_sound(char)

        return True

    def play_sound(widget, char):
        if widget.current_sound:
            widget.current_sound.stop()
            widget.current_sound = None

        sound_key = char.lower() if char.isalpha() else char
        sound = widget.asset_manager.get_sound(sound_key)
        if sound:
            def on_sound_stop(instance):
                instance.unload()
                if sound_key in widget.asset_manager.loaded_sounds:
                    del widget.asset_manager.loaded_sounds[sound_key]
                widget.current_sound = None

            sound.bind(on_stop=on_sound_stop)
            sound.play()
            widget.current_sound = sound

    def start_animation(self):
        anim = Animation(opacity=1, duration=0.5)
        anim += Animation(duration=0.8)
        anim += Animation(opacity=0, duration=1.0)
        anim.start(self.char_image)
        self.char_image.current_anim = anim


    def update(self, dt):
        pass

class GameApp(App):
    def build(self):
        Window.fullscreen = False
        return GameWidget()

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.loaded_sounds = {}
        self.load_images("assets/images")
        self.load_sounds("assets/sounds")

    def load_images(self, image_dir):
        # Load images
        if os.path.exists(image_dir):
            for filename in os.listdir(image_dir):
                if filename.endswith(".png"):
                    asset_name = filename.replace('.png', '')
                    self.images[asset_name] = os.path.join(image_dir, filename)

    def load_sounds(self, sound_dir):
        if os.path.exists(sound_dir):
            for filename in os.listdir(sound_dir):
                if filename.endswith(".mp3"):
                    asset_name = filename.replace('.mp3', '')
                    self.sounds[asset_name] = os.path.join(sound_dir, filename)

    def get_sound(self, asset_name):
        if asset_name in self.loaded_sounds:
            return self.loaded_sounds[asset_name]

        sound_path = self.sounds.get(asset_name)
        if sound_path and os.path.exists(sound_path):
            sound = SoundLoader.load(sound_path)
            if sound:
                self.loaded_sounds[asset_name] = sound
                return sound
        return None

def load_background_image(self):
    self.bg = Image(source="./assets/images/background/mountains_purple_trees.png", size=(1920, 1080), fit_mode="contain")
    self.add_widget(self.bg)

def load_background_music(self):
    # Background music
    self.music = SoundLoader.load("./assets/sounds/background/moonlight.mp3")
    self.music.loop = True
    # self.music.play()

def add_image_widget(self):
    self.char_image = Image(size=(1800, 900), fit_mode="contain", opacity=0)
    self.char_image.center = (Window.size[0] / 2, Window.size[1] / 2)
    self.char_image.current_anim = None
    self.add_widget(self.char_image)

if __name__ == "__main__":
    GameApp().run()
