from kivy.animation import Animation

def start_animation(image):
    anim = Animation(opacity=1, duration=0.5)
    anim += Animation(duration=0.8)
    anim += Animation(opacity=0, duration=1.0)
    anim.start(image)
    image.current_anim = anim
