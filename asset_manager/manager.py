import os
from kivy.core.audio import SoundLoader
from .config import IMAGE_DIR, SOUND_DIR


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
