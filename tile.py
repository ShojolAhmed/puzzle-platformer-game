import pygame
import settings

class Tile:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())

    def draw(self, screen):
        # pygame.draw.rect(screen, (0,255,0), self.rect, 1)
        screen.blit(self.image, self.rect)