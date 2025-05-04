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

        self.asset_manager = AssetManager()
        self.fade_images = {}  # Store Image widgets for each character

        # Load mountains PNG background
        self.bg = Image(source="./assets/images/background/mountains_purple_trees.png", size=(1920,1080), fit_mode="contain")

        # add children widgets
        self.add_widget(self.bg)

        # add background music to ensure it's running
        self.music = SoundLoader.load("./assets/sounds/background/moonlight.mp3")
        self.music.loop = True
        self.music.play()

        # Bind keyboard input
        Window.bind(on_key_down=self.on_keystroke_down)

        # Update for smooth movement
        Clock.schedule_interval(self.update, 1.0 / 60.0)  # 60 FPS

    def on_keystroke_down(self, window, key, scancode, codepoint, modifier):
        # print(f"key: {key} scancode: {scancode} codepoint: {codepoint} modifier: {modifier}")

        if codepoint and codepoint.isalpha():
            is_upper = codepoint.isupper()
            char = codepoint.lower()

            if char not in self.fade_images:
                img_path = self.asset_manager.get_image(char, is_upper)
                self.fade_images[char] = Image(source=img_path, size=(1800,900), fit_mode="contain", opacity=0)
                self.fade_images[char].center = (self.bg.size[0] / 2, self.bg.size[1] / 2)
                self.add_widget(self.fade_images[char])

            sound = self.asset_manager.get_sound(char, is_upper)
            if sound:
                sound.play()

            anim = Animation(opacity=1, duration=0.5)
            anim += Animation(duration=0.8)
            anim += Animation(opacity=0, duration=1.0)
            anim.start(self.fade_images[char])

        if codepoint and codepoint.isdigit():
            num = codepoint
            if num not in self.fade_images:
                img_path = self.asset_manager.get_image(num)
                self.fade_images[num] = Image(source=img_path, size=(1800,900), fit_mode="contain", opacity=0)
                self.fade_images[num].center = (self.bg.size[0] / 2, self.bg.size[1] / 2)
                self.add_widget(self.fade_images[num])

            sound = self.asset_manager.get_sound(num)
            if sound:
                sound.play()

            anim = Animation(opacity=1, duration=0.5)
            anim += Animation(duration=0.8)
            anim += Animation(opacity=0, duration=1.0)
            anim.start(self.fade_images[num])

        if codepoint and not codepoint.isalnum():
            sym = codepoint
            if sym not in self.fade_images:
                img_path = self.asset_manager.get_image(sym)
                self.fade_images[sym] = Image(source=img_path, size=(1800,900), fit_mode="contain", opacity=0)
                self.fade_images[sym].center = (self.bg.size[0] / 2, self.bg.size[1] / 2)
                self.add_widget(self.fade_images[sym])

            sound = self.asset_manager.get_sound(sym)
            if sound:
                sound.play()

            anim = Animation(opacity=1, duration=0.5)
            anim += Animation(duration=0.8)
            anim += Animation(opacity=0, duration=1.0)
            anim.start(self.fade_images[sym])

        return True

    def on_key_up(window, key, scancode):
        # print(f"args: {args}")
        return True

    def update(self, dt):
        pass

class GameApp(App):
    def build(self):
        Window.fullscreen = True
        return GameWidget()

class AssetManager:
    def __init__(self):
        self.lower_images = {}
        self.upper_images = {}
        self.numbers = {}
        self.symbols = {}
        self.sounds = {}
        self.load_assets()

    def load_assets(self):
        # Map characters to image/audio files
        chars = "abcdefghijklmnopqrstuvwxyz"
        for char in chars:
            lower_img_path = f"assets/images/lower/lower_{char}.png"
            self.lower_images[f"lower_{char}"] = lower_img_path if os.path.exists(lower_img_path) else None

            upper_img_path = f"assets/images/upper/upper_{char}.png"
            self.upper_images[f"upper_{char}"] = upper_img_path if os.path.exists(upper_img_path) else None

            sound_path = f"assets/sounds/lower/lower_{char}.mp3"
            self.sounds[f"lower_{char}"] = SoundLoader.load(sound_path) if os.path.exists(sound_path) else None

        # Map numbers to image/audio files
        numbers = "0123456789"
        for num in numbers:
            num_path = f"assets/images/numbers/numbers_{num}.png"
            self.numbers[f"numbers_{num}"] = num_path if os.path.exists(num_path) else None

            sound_path = f"assets/sounds/numbers/numbers_{num}.mp3"
            self.sounds[f"numbers_{num}"] = SoundLoader.load(sound_path) if os.path.exists(sound_path) else None

        # Map symbols to image/audio files
        symbols = "!@#$%"
        for sym in symbols:
            sym_path = f"assets/images/symbols/symbols_{sym}.png"
            self.symbols[f"symbols_{sym}"] = sym_path if os.path.exists(sym_path) else None

            sound_path = f"assets/sounds/symbols/symbols_{sym}.mp3"
            self.sounds[f"symbols_{sym}"] = SoundLoader.load(sound_path) if os.path.exists(sound_path) else None

    def get_image(self, val, is_upper=False):
        if val.isalpha():
            if is_upper:
                key = f"upper_{val.lower()}"
                return self.upper_images.get(key)
            else:
                key = f"lower_{val.lower()}"
            return self.lower_images.get(key)
        if val.isdigit():
            print(f"line 128: we arrived, val is digit: {val}")
            key = f"numbers_{val}"
            return self.numbers.get(key)
        if val and not val.isalnum():
            key = f"symbols_{val}"
            return self.symbols.get(key)

    def get_sound(self, val, is_upper=False):
        if val.isalpha():
            key = f"lower_{val.lower()}"
            return self.sounds.get(key)
        if val.isdigit():
            key = f"numbers_{val}"
            return self.sounds.get(key)
        if val and not val.isalnum():
            key = f"symbols_{val}"
            return self.sounds.get(key)

if __name__ == "__main__":
    GameApp().run()
