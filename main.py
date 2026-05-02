import pygame
import settings
import assets

from player import Player
from level.level_manager import LevelManager
from game.state_manager import StateManager
from game.play_state import PlayState
from game.menu_state import MenuState
from game.game_completed_state import GameCompletedState

pygame.init()

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

assets.load_assets()

manager = StateManager()

# Add states
manager.add("play", lambda: PlayState(manager, Player(), LevelManager(), font))
manager.add("menu", lambda: MenuState(manager, font, screen))
manager.add("game_completed", lambda: GameCompletedState(manager, font))

manager.set_state("menu")  # start in menu

running = True
while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    manager.handle_events(events)
    manager.update()
    manager.draw(screen, clock)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()