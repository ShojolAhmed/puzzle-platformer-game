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
        self.has_key = False

        # self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.rect = pygame.Rect(self.x, self.y, 10 * settings.SCALE, 12 * settings.SCALE)
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.on_ground:
                self.vel_y = settings.JUMP_FORCE
                self.on_ground = False
                self.moving = True

    def is_moving(self):
        if self.vel_x > 1 or self.vel_x < -1:
            return True
        return False

    def update(self, tiles, map_width, map_height):
        keys = pygame.key.get_pressed()

        # self.vel_x = 0
        self.moving = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x = -settings.SPEED
            self.facing_right = False
            self.moving = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x = settings.SPEED
            self.facing_right = True
            self.moving = True
        else:
            if self.on_ground:
                self.vel_x *= 0.7
            else:
                self.vel_x *= 0.95
        # print(self.vel_y)

        # if keys[pygame.K_SPACE] and self.on_ground:
        #     self.vel_y = settings.JUMP_FORCE
        #     self.on_ground = False

        self.vel_y += settings.GRAVITY

        # Horizontal Collisions
        self.rect.x += self.vel_x
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel_x > 0:  # moving right
                    self.rect.right = tile.rect.left
                elif self.vel_x < 0:  # moving left
                    self.rect.left = tile.rect.right
        
        # Vertical Collisions
        self.rect.y += self.vel_y
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel_y > 0:  # falling
                    self.rect.bottom = tile.rect.top
                    self.vel_y = 0
                    self.on_ground = True

                elif self.vel_y < 0:  # hitting ceiling
                    self.rect.top = tile.rect.bottom
                    self.vel_y = 0

        self.x = self.rect.x
        self.y = self.rect.y

        # Prevent falling below map
        # if self.rect.bottom > map_height:
        #     self.rect.bottom = map_height
        #     self.vel_y = 0
        #     self.on_ground = True

        # Prevent going above map
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0

        # Prevent going outside left/right
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0

        if self.rect.right > map_width:
            self.rect.right = map_width
            self.vel_x = 0

        self.animate()

    def animate(self):
        frames = self.run_frames if self.is_moving() else self.idle_frames
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0
        self.image = frames[int(self.frame_index)]
        # flip if facing left
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, screen):
        # pygame.draw.rect(screen, (255,0,0), self.rect, 2)
        # screen.blit(self.image, self.rect)
        screen.blit(self.image, (self.rect.x - 11 * settings.SCALE, self.rect.y - 20 * settings.SCALE))