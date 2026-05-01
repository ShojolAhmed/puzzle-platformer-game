import pygame
import pytmx
import settings

from tile import Tile
from door import Door
from moving_platform import MovingPlatform


def load_level(path):
    draw_tiles = []
    collision_tiles = []
    key_objects = []
    doors = []
    killing_zones = []
    moving_platforms = []
    player_spawn = (100, 400)

    tmx_data = pytmx.load_pygame(path)

    tile_size = settings.TILE_SIZE
    scale = settings.SCALE

    # TILE LAYERS
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

    # OBJECT LAYERS
    for layer in tmx_data.layers:
        if isinstance(layer, pytmx.TiledObjectGroup):

            if layer.name == "PlayerSpawn":
                for obj in layer:
                    player_spawn = (int(obj.x * scale), int(obj.y * scale))
                    break

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

            if layer.name == "Doors":
                for obj in layer:
                    image = pygame.transform.scale(
                        obj.image,
                        (int(obj.width * scale), int(obj.height * scale))
                    )

                    doors.append(Door(int(obj.x * scale), int(obj.y * scale), image))

            if layer.name == "KillingZone":
                for obj in layer:
                    rect = pygame.Rect(
                        int(obj.x * scale),
                        int(obj.y * scale),
                        int(obj.width * scale),
                        int(obj.height * scale)
                    )
                    killing_zones.append(rect)

            if layer.name == "MovingPlatforms":
                for obj in layer:
                    image = pygame.transform.scale(
                        obj.image,
                        (int(obj.width * scale), int(obj.height * scale))
                    )

                    moving_platforms.append(
                        MovingPlatform(
                            int(obj.x * scale),
                            int(obj.y * scale),
                            int(obj.width * scale),
                            int(obj.height * scale),
                            image,
                            obj.properties.get("axis", "x"),
                            int(obj.properties.get("speed", 2)),
                            int(obj.properties.get("range", 5))
                        )
                    )

    return {
        "draw_tiles": draw_tiles,
        "collision_tiles": collision_tiles,
        "keys": key_objects,
        "doors": doors,
        "killing_zones": killing_zones,
        "platforms": moving_platforms,
        "spawn": player_spawn
    }