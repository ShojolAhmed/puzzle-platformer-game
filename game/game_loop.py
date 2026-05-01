import pygame
import settings

from systems.collision import is_on_platform
from systems.reset import reset_player

DEBUG = True


def run_game(screen, clock, player, level_manager, font):

    running = True

    while running:
        data = level_manager.data

        draw_tiles = data["draw_tiles"]
        collision_tiles = data["collision_tiles"]
        key_objects = data["keys"]
        doors = data["doors"]
        killing_zones = data["killing_zones"]
        platforms = data["platforms"]
        spawn = data["spawn"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            player.handle_events(event)

            # =========================
            # DEBUG CONTROLS
            # =========================
            if DEBUG and event.type == pygame.KEYDOWN:

                # Switch level (1–9)
                if pygame.K_1 <= event.key <= pygame.K_9:
                    index = event.key - pygame.K_1

                    if index < len(level_manager.LEVELS):
                        level_manager.current_level = index
                        level_manager.reload()

                        spawn = level_manager.data["spawn"]
                        reset_player(player, spawn)

                        print(f"Debug: Switched to level {index}")

                # Reset current level
                elif event.key == pygame.K_r:
                    level_manager.reload()

                    spawn = level_manager.data["spawn"]
                    reset_player(player, spawn)

                    print("Debug: Level reset")

        # =========================
        # UPDATE
        # =========================

        # Platforms
        for p in platforms:
            p.update()

        for p in platforms:
            if is_on_platform(player, p):
                dx, dy = p.get_movement()
                player.rect.x += dx
                player.rect.y += dy

        # Doors
        for door in doors:
            door.update(player, lambda: handle_next_level(level_manager, player))

        # Player update
        colliders = (
            collision_tiles
            + [d for d in doors if not d.is_open]
            + platforms
        )

        player.update(colliders, settings.WIDTH, settings.HEIGHT)

        # Killing zones
        for zone in killing_zones:
            if player.rect.colliderect(zone):
                print("Player died!")

                level_manager.reload()
                reset_player(player, spawn)
                break

        # Keys
        for key in key_objects[:]:
            if player.rect.colliderect(key["rect"]):
                print("Key collected!")
                player.has_key = True
                key_objects.remove(key)

        # =========================
        # DRAW
        # =========================
        screen.fill((30, 30, 30))

        for t in draw_tiles:
            t.draw(screen)

        for p in platforms:
            p.draw(screen)

        for key in key_objects:
            screen.blit(key["image"], key["rect"])

        for door in doors:
            door.draw(screen)

        player.draw(screen)

        fps = int(clock.get_fps())
        screen.blit(font.render(f"FPS: {fps}", True, (255, 255, 255)), (10, 10))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()


def handle_next_level(level_manager, player):
    if not level_manager.next_level():
        print("Game Completed!")
        pygame.quit()
        exit()

    reset_player(player, level_manager.data["spawn"])