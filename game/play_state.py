import pygame
import settings

from systems.collision import is_on_platform
from systems.reset import reset_player


class PlayState:
    def __init__(self, manager, player, level_manager, font):
        self.manager = manager
        self.player = player
        self.level_manager = level_manager
        self.font = font

        # spawn player
        spawn = self.level_manager.data["spawn"]
        self.player.rect.x, self.player.rect.y = spawn

    def handle_events(self, events):
        for event in events:

            self.player.handle_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.manager.set_state("menu")

            # DEBUG CONTROLS
            if settings.DEBUG and event.type == pygame.KEYDOWN:

                if pygame.K_1 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_1

                    if index < len(self.level_manager.LEVELS):
                        self.level_manager.current_level = index
                        self.level_manager.reload()

                        spawn = self.level_manager.data["spawn"]
                        reset_player(self.player, spawn)

                elif event.key == pygame.K_r:
                    self.level_manager.reload()

                    spawn = self.level_manager.data["spawn"]
                    reset_player(self.player, spawn)

    def update(self):
        data = self.level_manager.data

        collision_tiles = data["collision_tiles"]
        doors = data["doors"]
        killing_zones = data["killing_zones"]
        platforms = data["platforms"]
        spawn = data["spawn"]

        # Platforms
        for p in platforms:
            p.update()

        for p in platforms:
            if is_on_platform(self.player, p):
                dx, dy = p.get_movement()
                self.player.rect.x += dx
                self.player.rect.y += dy

        # Doors
        for door in doors:
            door.update(self.player, lambda: self.next_level())

        # Player update
        colliders = (
            collision_tiles
            + [d for d in doors if not d.is_open]
            + platforms
        )

        self.player.update(colliders, settings.WIDTH, settings.HEIGHT)

        # Killing zones
        for zone in killing_zones:
            if self.player.rect.colliderect(zone):
                self.level_manager.reload()
                reset_player(self.player, spawn)
                break

        # Keys
        for key in data["keys"][:]:
            if self.player.rect.colliderect(key["rect"]):
                self.player.has_key = True
                data["keys"].remove(key)

    def draw(self, screen, clock):
        data = self.level_manager.data

        screen.fill((30, 30, 30))

        for t in data["draw_tiles"]:
            t.draw(screen)

        for p in data["platforms"]:
            p.draw(screen)

        for key in data["keys"]:
            screen.blit(key["image"], key["rect"])

        for door in data["doors"]:
            door.draw(screen)

        self.player.draw(screen)

        if settings.DEBUG:
            fps = int(clock.get_fps())
            screen.blit(self.font.render(f"FPS: {fps}", True, (255, 255, 255)), (10, 10))

    def next_level(self):
        if not self.level_manager.next_level():
            print("Game Completed!")
            self.manager.set_state("game_completed")
            return

        reset_player(self.player, self.level_manager.data["spawn"])