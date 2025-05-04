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
        self.images = {}
        self.sounds = {}
        self.load_assets()

    def load_assets(self):
        # Map characters to image/audio files
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%"
        for char in chars:
            # Lowercase
            img_path = f"assets/images/lower/lower_{char}.png"
            sound_path = f"assets/sounds/lower/lower_{char}.mp3"
            self.images[f"lower_{char}"] = img_path if os.path.exists(img_path) else None
            self.sounds[f"lower_{char}"] = SoundLoader.load(sound_path) if os.path.exists(sound_path) else None

            if char.isalpha():
                img_path = f"assets/images/upper/upper_{char}.png"
                sound_path = f"assets/sounds/upper/upper_{char}.mp3"
                self.images[f"upper_{char}"] = img_path if os.path.exists(img_path) else None
                self.sounds[f"upper_{char}"] = SoundLoader.load(sound_path) if os.path.exists(sound_path) else None

            # try:
            #     self.images[f"lower_{char}"] = f"assets/images/lower/lower_{char}.png"
            #     self.sounds[f"lower_{char}"] = SoundLoader.load(f"assets/sounds/lower/lower_{char}.mp3")
            # except Exception as e:
            #     print(f"Skipping lower_{char}: {e}")
            #     self.images[f"lower_{char}"] = None
            #     self.sounds[f"lower_{char}"] = None
            # # Uppercase
            # if char.isalpha():
            #     try:
            #         self.images[f"upper_{char}"] = f"assets/images/upper_{char}.png"
            #         self.sounds[f"upper_{char}"] = SoundLoader.load(f"assets/sounds/upper/upper_{char}.mp3")
            #     except Exception as e:
            #         print(f"Skipping upper_{char}: {e}")
            #         self.images[f"upper_{char}"] = None
            #         self.sounds[f"upper_{char}"] = None

    def get_image(self, char, is_upper=False):
        key = f"upper_{char.lower()}" if is_upper else f"lower_{char.lower()}"
        return self.images.get(key)

    def get_sound(self, char, is_upper=False):
        key = f"upper_{char.lower()}" if is_upper else f"lower_{char.lower()}"
        return self.sounds.get(key)

if __name__ == "__main__":
    GameApp().run()
