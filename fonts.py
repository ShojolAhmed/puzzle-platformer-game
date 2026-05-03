import pygame

class Fonts:
    def __init__(self):
        # UI fonts
        self.ui_small = pygame.font.Font("assets/fonts/RobotoCondensed-Regular.ttf", 24)
        self.ui_medium = pygame.font.Font("assets/fonts/RobotoCondensed-Regular.ttf", 32)
        self.ui_bold = pygame.font.Font("assets/fonts/RobotoCondensed-Bold.ttf", 40)

        # Timer / HUD
        self.timer = pygame.font.Font("assets/fonts/JetBrainsMono-Regular.ttf", 28)
        self.debug = pygame.font.Font("assets/fonts/JetBrainsMono-Regular.ttf", 20)

        # Titles
        self.title = pygame.font.Font("assets/fonts/BebasNeue-Regular.ttf", 72)