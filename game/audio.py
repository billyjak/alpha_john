from kivy.core.audio import SoundLoader
from asset_manager.config import BACKGROUND_MUSIC_PATH

def setup_audio(widget):
    # Background music
    widget.music = SoundLoader.load(BACKGROUND_MUSIC_PATH)
    widget.music.loop = True
    # widget.music.play()

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

