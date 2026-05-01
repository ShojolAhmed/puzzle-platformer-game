import pygame
from settings import TILE_SIZE

class MovingPlatform:
    def __init__(self, x, y, w, h, image, axis="x", speed=2, range_tiles=5):
        self.rect = pygame.Rect(x, y, w, h)
        self.image = image

        self.axis = axis
        self.speed = speed

        # convert TILE range → PIXELS
        self.range = range_tiles * TILE_SIZE

        self.prev_x = x
        self.prev_y = y

        self.start_x = x
        self.start_y = y

        self.direction = 1

    def update(self):
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y

        if self.axis == "x":
            self.rect.x += self.speed * self.direction

            if abs(self.rect.x - self.start_x) >= self.range:
                self.direction *= -1

        else:
            self.rect.y += self.speed * self.direction

            if abs(self.rect.y - self.start_y) >= self.range:
                self.direction *= -1

    def get_movement(self):
        return self.rect.x - self.prev_x, self.rect.y - self.prev_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)