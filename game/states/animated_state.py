class AnimatedState:
    def __init__(self):
        self.alpha = 0
        self.slide_offset = 40
        self.anim_speed = 10

    def update_animation(self):
        if self.alpha < 255:
            self.alpha += self.anim_speed

        if self.slide_offset > 0:
            self.slide_offset -= 2