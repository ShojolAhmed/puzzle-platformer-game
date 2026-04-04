import pygame
import pytmx
import settings
import assets
from player import Player
from tile import Tile

pygame.init()

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)

assets.load_assets()

player = Player()

tmx_data = pytmx.load_pygame("maps/testMap.tmx")

draw_tiles = []
collision_tiles = []
tile_size = settings.TILE_SIZE
scale = settings.SCALE

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

                # draw everything
                draw_tiles.append(tile)

                # only ground collides
                if layer.name == "Ground":
                    collision_tiles.append(tile)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        player.handle_events(event)

    player.update(collision_tiles)

    # for updating each frame
    screen.fill((30,30,30))

    # show fps count
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255,255,255))

    for tile in draw_tiles:
        tile.draw(screen)
    player.draw(screen)
    screen.blit(fps_text,(10,10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()