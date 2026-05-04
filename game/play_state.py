import pygame
import settings

from systems.reset import reset_player
from systems.speedrun_timer import SpeedrunTimer


class PlayState:
    def __init__(self, manager, player, level_manager, font):
        self.manager = manager
        self.player = player
        self.level_manager = level_manager
        self.font = font

        self.timer = SpeedrunTimer()
        self.timer.start()

        # spawn player
        spawn = self.level_manager.data["spawn"]
        self.player.rect.x, self.player.rect.y = spawn

    def handle_events(self, events):
        for event in events:

            self.player.handle_events(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.timer.stop()  # pause timer
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
        self.timer.update()

        data = self.level_manager.data

        collision_tiles = data["collision_tiles"]
        doors = data["doors"]
        killing_zones = data["killing_zones"]
        platforms = data["platforms"]
        spawn = data["spawn"]

        # =========================
        # UPDATE PLATFORMS FIRST
        # =========================
        for p in platforms:
            p.update()

        # =========================
        # DOORS
        # =========================
        for door in doors:
            door.update(self.player, lambda: self.next_level())

        # =========================
        # PLAYER UPDATE
        # (platforms passed separately)
        # =========================
        colliders = (
            collision_tiles
            + [d for d in doors if not d.is_open]
        )

        self.player.update(colliders, platforms, settings.WIDTH, settings.HEIGHT)

        # =========================
        # KILLING ZONES
        # =========================
        for zone in killing_zones:
            if self.player.rect.colliderect(zone):
                self.level_manager.reload()
                reset_player(self.player, spawn)
                break

        # =========================
        # KEYS
        # =========================
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

        for t in data["texts"]:
            if not self.player.has_key and not t["hidden"]:
                screen.blit(self.font.timer.render(t["text"], True, (255, 255, 255)), t["pos"])
                break
            if t["hidden"]:
                screen.blit(self.font.timer.render(t["text"], True, (255, 255, 255)), t["pos"])

            # pygame.draw.circle(screen, (255, 0, 0), t["pos"], 5)

        self.player.draw(screen)

        # =========================
        # TIMER UI
        # =========================
        t = self.timer.get_time()

        minutes = int(t // 60)
        seconds = int(t % 60)
        ms = int((t - int(t)) * 100)

        timer_text = self.font.timer.render(
            f"{minutes:02}:{seconds:02}.{ms:02}",
            True,
            (255, 255, 255)
        )

        timer_rect = timer_text.get_rect(
            midtop=(settings.WIDTH // 2, 10)
        )

        padding = 8
        bg_rect = timer_rect.inflate(padding * 2, padding)

        bg = pygame.Surface(bg_rect.size)
        bg.set_alpha(120)
        bg.fill((0, 0, 0))
        screen.blit(bg, bg_rect.topleft)

        screen.blit(timer_text, timer_rect)

        # =========================
        # DEBUG
        # =========================
        if settings.DEBUG:
            fps = int(clock.get_fps())
            screen.blit(
                self.font.timer.render(f"FPS: {fps}", True, (255, 255, 255)),
                (10, 10)
            )

    def next_level(self):
        if not self.level_manager.next_level():
            self.timer.stop()

            final_time = self.timer.get_time()
            self.manager.final_time = final_time

            self.manager.set_state("name_input")
            return

        reset_player(self.player, self.level_manager.data["spawn"])