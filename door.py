import pygame

class Door:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.is_open = False

    def update(self, player, on_open_callback):

        if self.is_open:
            return

        if self.rect.colliderect(player.rect.inflate(40, 40)):
            keys = pygame.key.get_pressed()

            if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.has_key:
                print("Door opened!")
                self.is_open = True
                on_open_callback()

    def draw(self, screen):
        if not self.is_open:
            screen.blit(self.image, self.rect)