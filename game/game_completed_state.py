import pygame
import ui_theme as theme
import ui_text as ui
from game.ui.button import Button
from game.states.animated_state import AnimatedState

class GameCompletedState(AnimatedState):
    def __init__(self, manager, font, screen):
        super().__init__()

        self.manager = manager
        self.font = font
        self.screen = screen

        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2

        self.button = Button(
            ui.BUTTON_BACK_TO_MENU,
            (center_x, center_y + 80),
            (260, 55),
            font.ui_medium,
            self.go_to_menu
        )

    def go_to_menu(self):
        self.manager.clear_game()
        self.manager.set_state("menu")

    def handle_events(self, events):
        for event in events:
            self.button.handle_event(event)

    def update(self):
        self.update_animation()
        self.button.update()

    def draw(self, screen, clock):
        screen.fill((10, 10, 18))

        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2

        # TITLE with slide animation
        text = self.font.title.render(ui.GAME_COMPLETED_TITLE, True, (255, 255, 255))
        text_rect = text.get_rect(center=(center_x, center_y - 100 - self.slide_offset))
        screen.blit(text, text_rect)

        # button animation offset
        self.button.rect.center = (center_x, center_y + 60 + self.slide_offset)
        self.button.draw(screen)

        # fade-in overlay (IMPORTANT)
        fade = pygame.Surface(screen.get_size())
        fade.set_alpha(255 - self.alpha)
        fade.fill((0, 0, 0))
        screen.blit(fade, (0, 0))

        # speedrun time
        t = self.manager.final_time

        minutes = int(t // 60)
        seconds = int(t % 60)
        ms = int((t - int(t)) * 100)

        time_text = self.font.timer.render(
            f"Time: {minutes:02}:{seconds:02}.{ms:02}",
            True,
            (200, 200, 200)
        )

        screen.blit(time_text, (center_x - 80, center_y - 20))