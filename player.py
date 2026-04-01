import pygame
import settings
import assets

class Player:
    def __init__(self):
        # Load frames
        self.idle_frames = assets.get_frames(row=0, cols=4, size=settings.SPRITE_SIZE, scale=settings.SCALE)
        self.run_frames = assets.get_frames(row=4, cols=8, size=settings.SPRITE_SIZE, scale=settings.SCALE)

        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.idle_frames[0]

        self.x = 100
        self.y = 400

        self.vel_x = 0
        self.vel_y = 0

        self.on_ground = False
        self.facing_right = True
        self.moving = False

    def update(self):
        keys = pygame.key.get_pressed()

        self.vel_x = 0
        self.moving = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -settings.SPEED
            self.facing_right = False
            self.moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = settings.SPEED
            self.facing_right = True
            self.moving = True

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = settings.JUMP_FORCE
            self.on_ground = False

        self.vel_y += settings.GRAVITY

        self.x += self.vel_x
        self.y += self.vel_y

        if self.y >= settings.GROUND_Y:
            self.y = settings.GROUND_Y
            self.vel_y = 0
            self.on_ground = True

        self.animate()

    def animate(self):
        frames = self.run_frames if self.moving else self.idle_frames
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0
        self.image = frames[int(self.frame_index)]
        # flip if facing left
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))