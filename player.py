import pygame
import settings
import assets


class Player:
    def __init__(self):
        # Load frames
        self.idle_frames = assets.get_frames(row=0, cols=4, size=settings.SPRITE_SIZE, scale=settings.SCALE)
        self.run_frames = assets.get_frames(row=4, cols=8, size=settings.SPRITE_SIZE, scale=settings.SCALE)
        self.jump_up_frame = assets.get_frames(row=8, cols=4, size=settings.SPRITE_SIZE, scale=settings.SCALE)[1]
        self.fall_frame = assets.get_frames(row=8, cols=4, size=settings.SPRITE_SIZE, scale=settings.SCALE)[3]

        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.idle_frames[0]

        self.coyote_time = 0
        self.max_coyote_time = 6

        self.jump_buffer_time = 0
        self.max_jump_buffer_time = 6

        self.x = 100
        self.y = 400

        self.vel_x = 0
        self.vel_y = 0

        self.on_ground = False
        self.facing_right = True
        self.moving = False
        self.has_key = False

        # Platform tracking
        self.current_platform = None

        self.rect = pygame.Rect(self.x, self.y, 10 * settings.SCALE, 12 * settings.SCALE)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.jump_buffer_time = self.max_jump_buffer_time

    def is_moving(self):
        return abs(self.vel_x) > 1

    def update(self, tiles, moving_platforms, map_width, map_height):
        keys = pygame.key.get_pressed()

        # =========================
        # TIMER UPDATES
        # =========================
        self.coyote_time = max(0, self.coyote_time - 1)
        self.jump_buffer_time = max(0, self.jump_buffer_time - 1)

        self.moving = False

        # =========================
        # HORIZONTAL MOVEMENT
        # =========================
        left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

        if left and right:
            self.vel_x = 0
        elif left:
            self.vel_x = -settings.SPEED
            self.facing_right = False
            self.moving = True
        elif right:
            self.vel_x = settings.SPEED
            self.facing_right = True
            self.moving = True
        else:
            if self.on_ground:
                self.vel_x *= 0.7
            else:
                self.vel_x *= 0.95

        # =========================
        # GRAVITY
        # =========================
        self.vel_y += settings.GRAVITY

        # =========================
        # APPLY HORIZONTAL COLLISION (TILES ONLY)
        # =========================
        self.rect.x += self.vel_x

        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel_x > 0:
                    self.rect.right = tile.rect.left
                elif self.vel_x < 0:
                    self.rect.left = tile.rect.right

        # =========================
        # APPLY VERTICAL MOVEMENT
        # =========================
        self.rect.y += self.vel_y
        self.on_ground = False
        self.current_platform = None

        # =========================
        # TILE COLLISION (VERTICAL)
        # =========================
        for tile in tiles:
            if self.rect.colliderect(tile.rect):

                if self.vel_y > 0:  # falling
                    self.rect.bottom = tile.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.coyote_time = self.max_coyote_time

                elif self.vel_y < 0:  # hitting ceiling
                    self.rect.top = tile.rect.bottom
                    self.vel_y = 0

        # =========================
        # PLATFORM COLLISION (VERTICAL ONLY)
        # =========================
        for platform in moving_platforms:
            if self.rect.colliderect(platform.rect):

                # Only land when falling onto platform
                if self.vel_y > 0 and self.rect.bottom <= platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.coyote_time = self.max_coyote_time
                    self.current_platform = platform

        # =========================
        # APPLY PLATFORM MOVEMENT
        # =========================
        if self.on_ground and self.current_platform:
            dx, dy = self.current_platform.get_movement()
            self.rect.x += dx
            self.rect.y += dy

        # =========================
        # BUFFERED + COYOTE JUMP
        # =========================
        if self.jump_buffer_time > 0 and self.coyote_time > 0:
            self.vel_y = settings.JUMP_FORCE
            self.on_ground = False
            self.coyote_time = 0
            self.jump_buffer_time = 0
            self.current_platform = None

        # =========================
        # WORLD BOUNDS
        # =========================
        self.x = self.rect.x
        self.y = self.rect.y

        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0

        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x = 0

        if self.rect.right > map_width:
            self.rect.right = map_width
            self.vel_x = 0

        # =========================
        # ANIMATION
        # =========================
        self.animate()

    def animate(self):
        # AIR animation (optional, you commented it before)
        if not self.on_ground:
            if self.vel_y < 0:
                self.image = self.jump_up_frame
            else:
                self.image = self.fall_frame
        else:
            frames = self.run_frames if self.is_moving() else self.idle_frames
            self.frame_index += self.animation_speed
            if self.frame_index >= len(frames):
                self.frame_index = 0
            self.image = frames[int(self.frame_index)]

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x - 11 * settings.SCALE, self.rect.y - 20 * settings.SCALE))