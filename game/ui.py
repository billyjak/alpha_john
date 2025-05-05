from kivy.uix.image import Image
from kivy.core.window import Window
from asset_manager.config import BACKGROUND_IMAGE_PATH

def setup_ui(widget):
    widget.bg = Image(source=BACKGROUND_IMAGE_PATH, size=(1920, 1080), fit_mode="contain")
    widget.add_widget(widget.bg)

    widget.char_image = Image(size=(1800, 900), fit_mode="contain", opacity=0)
    widget.char_image.center = (Window.size[0] / 2, Window.size[1] / 2)
    widget.char_image.current_anim = None
    widget.add_widget(widget.char_image)
