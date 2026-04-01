import pygame
import settings
import assets
from player import Player

pygame.init()

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)

assets.load_assets()

player = Player()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update()

    # for updating each frame
    screen.fill((30,30,30))

    # show fps count
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, (255,255,255))

    player.draw(screen)
    screen.blit(fps_text,(10,10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()