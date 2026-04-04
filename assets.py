import pygame
import settings

sprite_sheet = None
tile_sheet = None

def load_assets():
    global sprite_sheet
    sprite_sheet = pygame.image.load("assets/sprites/cat_sprite_sheet.png").convert_alpha()

    global tile_sheet
    tile_sheet = pygame.image.load("assets/tiles/tilesheet1.png").convert_alpha()


# def get_player_sprite(size, scale):
#     sprite = sprite_sheet.subsurface((0,0,size,size))
#     sprite = pygame.transform.scale(sprite, (size*scale, size*scale))
#     return sprite

def get_frames(row, cols, size, scale):
    """
    Get all frames from a specific row.
    row: row index (0-based)
    cols: number of columns in the row
    size: original sprite size
    scale: how much to scale
    Returns a list of pygame.Surface
    """
    frames = []
    for col in range(cols):
        frame = sprite_sheet.subsurface((col*size, row*size, size, size))
        frame = pygame.transform.scale(frame, (size*scale, size*scale))
        frames.append(frame)
    return frames

def get_tile(x, y, tile_size, scale):
    """Get a single tile from the sheet (x,y in grid coords)"""
    tile = tile_sheet.subsurface((x*tile_size, y*tile_size, tile_size, tile_size))
    tile = pygame.transform.scale(tile, (tile_size*scale, tile_size*scale))
    return tile

def get_tile_list(rows, cols, tile_size, scale):
    """Return all tiles as a list"""
    tiles = []
    for y in range(rows):
        for x in range(cols):
            tiles.append(get_tile(x, y, tile_size, scale))
    return tiles