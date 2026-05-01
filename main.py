import pygame
import pytmx
import settings
import assets

from player import Player
from tile import Tile
from door import Door
from moving_platform import MovingPlatform

pygame.init()

pygame.display.set_caption("DEV_WINDOW")
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)

assets.load_assets()

# =========================
# LEVEL SYSTEM
# =========================
LEVELS = [
    "maps/testMap.tmx",
    "maps/level2.tmx",
    "maps/level3.tmx"
]

current_level = 0

# game objects
draw_tiles = []
collision_tiles = []
key_objects = []
doors = []
killing_zones = []
moving_platforms = []

player = Player()
player_spawn = (100, 400)


# =========================
# LOAD LEVEL FUNCTION
# =========================
def load_level(index):
    global draw_tiles, collision_tiles, key_objects, doors, killing_zones, player_spawn, moving_platforms

    draw_tiles = []
    collision_tiles = []
    key_objects = []
    doors = []
    killing_zones = []
    moving_platforms = []


    tmx_data = pytmx.load_pygame(LEVELS[index])

    tile_size = settings.TILE_SIZE
    scale = settings.SCALE

    # -------- TILE LAYERS --------
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):

            for x, y, gid in layer:
                tile_image = tmx_data.get_tile_image_by_gid(gid)

                if tile_image:
                    tile_image = pygame.transform.scale(
                        tile_image,
                        (tile_size * scale, tile_size * scale)
                    )

                    world_x = x * tile_size * scale
                    world_y = y * tile_size * scale

                    tile = Tile(world_x, world_y, tile_image)

                    draw_tiles.append(tile)

                    if layer.name == "Ground":
                        collision_tiles.append(tile)


    # -------- OBJECT LAYERS --------
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup):

            # PLAYER SPAWN
            if layer.name == "PlayerSpawn":
                for obj in layer:
                    player_spawn = (int(obj.x * scale), int(obj.y * scale))
                    break

            # KEY
            if layer.name == "Keys":
                for obj in layer:
                    image = pygame.transform.scale(
                        obj.image,
                        (int(obj.width * scale), int(obj.height * scale))
                    )

                    x = int(obj.x * scale)
                    y = int(obj.y * scale)

                    key_objects.append({
                        "rect": pygame.Rect(x, y, image.get_width(), image.get_height()),
                        "image": image
                    })

            # DOOR
            if layer.name == "Doors":
                for obj in layer:
                    image = pygame.transform.scale(
                        obj.image,
                        (int(obj.width * scale), int(obj.height * scale))
                    )

                    x = int(obj.x * scale)
                    y = int(obj.y * scale)

                    doors.append(Door(x, y, image))

            # KILLING ZONE
            if layer.name == "KillingZone":
                for obj in layer:
                    x = int(obj.x * scale)
                    y = int(obj.y * scale)
                    w = int(obj.width * scale)
                    h = int(obj.height * scale)

                    rect = pygame.Rect(x, y, w, h)
                    killing_zones.append(rect)

            # MOVING PLATFORMS
            if layer.name == "MovingPlatforms":
                for obj in layer:
                    image = pygame.transform.scale(
                        obj.image,
                        (int(obj.width * scale), int(obj.height * scale))
                    )

                    x = int(obj.x * scale)
                    y = int(obj.y * scale)
                    w = int(obj.width * scale)
                    h = int(obj.height * scale)

                    axis = obj.properties.get("axis", "x")
                    speed = int(obj.properties.get("speed", 2))
                    range_tiles = int(obj.properties.get("range", 5))

                    moving_platforms.append(
                        MovingPlatform(x, y, w, h, image, axis, speed, range_tiles)
                    )


def is_on_platform(player, platform):
    test_rect = player.rect.copy()
    test_rect.y += 2  # small downward probe
    return test_rect.colliderect(platform.rect)


def reset_player():
    # player.rect.x = 100
    # player.rect.y = 400
    player.rect.x, player.rect.y = player_spawn
    player.vel_x = 0
    player.vel_y = 0
    player.has_key = False

# =========================
# NEXT LEVEL FUNCTION
# =========================
def next_level():
    global current_level, player

    current_level += 1

    if current_level >= len(LEVELS):
        print("Game Completed!")
        pygame.quit()
        exit()

    print(f"Loading level {current_level}")
    load_level(current_level)

    # reset player
    reset_player()


# =========================
# INIT FIRST LEVEL
# =========================
load_level(current_level)
player.rect.x, player.rect.y = player_spawn


# =========================
# GAME LOOP
# =========================
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        player.handle_events(event)


        # ----------------------------------
        # FOR DEBUG ONLY
        # ----------------------------------
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_9:
                index = event.key - pygame.K_1

                if index < len(LEVELS):
                    current_level = index
                    print(f"Debug: Switching to level {index}")

                    load_level(current_level)
                    reset_player()

            elif event.key == pygame.K_r:
                load_level(current_level)
                reset_player()


    # Platforms
    for platform in moving_platforms:
        platform.update()

    for platform in moving_platforms:
        if is_on_platform(player, platform):
            dx, dy = platform.get_movement()
            player.rect.x += dx
            player.rect.y += dy

    # -------------------------
    # DOORS
    # -------------------------
    for door in doors:
        door.update(player, next_level)


    # # Ride Player with the Platform
    # for platform in moving_platforms:
    #     if player.rect.colliderect(platform.rect):
    #
    #         if platform.axis == "x":
    #             player.rect.x += platform.speed * platform.direction
    #         else:
    #             player.rect.y += platform.speed * platform.direction


    door_colliders = [door for door in doors if not door.is_open]
    platform_colliders = [p for p in moving_platforms]

    player.update(
        collision_tiles + [d for d in door_colliders] + platform_colliders,
        settings.WIDTH,
        settings.HEIGHT
    )

    # -------------------------
    # KILLING ZONE COLLISION
    # -------------------------
    for zone in killing_zones:
        if player.rect.colliderect(zone):
            print("Player died!")
            load_level(current_level)
            reset_player()

            break

    # -------------------------
    # KEY COLLISION
    # -------------------------
    for key in key_objects[:]:
        if player.rect.colliderect(key["rect"]):
            print("Key collected!")
            player.has_key = True
            key_objects.remove(key)

    # =========================
    # DRAW
    # =========================
    screen.fill((30, 30, 30))

    for tile in draw_tiles:
        tile.draw(screen)

    for platform in moving_platforms:
        platform.draw(screen)

    for key in key_objects:
        screen.blit(key["image"], key["rect"])

    for door in doors:
        door.draw(screen)

    # for zone in killing_zones:
    #     pygame.draw.rect(screen, (255, 0, 0), zone, 2)

    player.draw(screen)

    fps = int(clock.get_fps())
    screen.blit(font.render(f"FPS: {fps}", True, (255, 255, 255)), (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()