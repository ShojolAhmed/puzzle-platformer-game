import pygame
from game.ui.button import Button
import ui_text as ui


class GameCompletedState:
    def __init__(self, manager, font):
        self.manager = manager
        self.font = font

        self.button = Button(
            ui.BUTTON_BACK_TO_MENU,
            (300, 320),
            (200, 50),
            font,
            self.go_to_menu
        )

    def go_to_menu(self):
        self.manager.clear_game()  # ← no more continue
        self.manager.set_state("menu")

    def handle_events(self, events):
        for event in events:
            self.button.handle_event(event)

    def update(self):
        pass

    def draw(self, screen, clock):
        screen.fill((10, 10, 10))

        center_x = screen.get_width() // 2
        center_y = screen.get_height() // 2

        text = self.font.render(ui.GAME_COMPLETED_TITLE, True, (255, 255, 255))
        text_rect = text.get_rect(center=(center_x, center_y - 80))
        screen.blit(text, text_rect)

        # center button
        self.button.rect.center = (center_x, center_y + 40)

        self.button.draw(screen)