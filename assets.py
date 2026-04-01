import pygame
import settings

sprite_sheet = None

def load_assets():
    global sprite_sheet
    sprite_sheet = pygame.image.load("assets/sprites/cat_sprite_sheet.png").convert_alpha()


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
    """
    frames = []
    for col in range(cols):
        frame = sprite_sheet.subsurface((col*size, row*size, size, size))
        frame = pygame.transform.scale(frame, (size*scale, size*scale))
        frames.append(frame)
    return frames