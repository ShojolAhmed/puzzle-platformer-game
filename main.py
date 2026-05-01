import pygame
import settings
import assets

from player import Player
from level.level_manager import LevelManager
from game.game_loop import run_game

pygame.init()

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("DEV_WINDOW")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

assets.load_assets()

player = Player()
level_manager = LevelManager()

# spawn player
spawn = level_manager.data["spawn"]
player.rect.x, player.rect.y = spawn

run_game(screen, clock, player, level_manager, font)