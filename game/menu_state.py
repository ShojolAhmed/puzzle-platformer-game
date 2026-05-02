from game.ui.button import Button
import pygame
import ui_text as ui


class MenuState:
    def __init__(self, manager, font, screen):
        self.manager = manager
        self.font = font
        self.screen = screen

        self.build_buttons()

    def build_buttons(self):
        self.buttons = []

        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        spacing = 70
        y = center_y

        if self.manager.has_active_game():
            self.buttons.append(
                Button(ui.BUTTON_CONTINUE, (center_x, y), (220, 50), self.font, self.continue_game)
            )
            y += spacing

        self.buttons.append(
            Button(ui.BUTTON_START, (center_x, y), (220, 50), self.font, self.start_game)
        )
        y += spacing

        self.buttons.append(
            Button(ui.BUTTON_SCOREBOARD, (center_x, y), (220, 50), self.font, self.scoreboard)
        )
        y += spacing

        self.buttons.append(
            Button(ui.BUTTON_QUIT, (center_x, y), (220, 50), self.font, self.quit_game)
        )

    def start_game(self):
        # create fresh game
        play = self.manager.states["play"]()
        self.manager.set_play_state(play)

    def continue_game(self):
        self.manager.continue_game()

    def scoreboard(self):
        print("Scoreboard coming soon...")

    def quit_game(self):
        pygame.quit()
        exit()

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

    def update(self):
        pass

    def draw(self, screen, clock):
        screen.fill((20, 20, 20))

        title = self.font.render(ui.MENU_TITLE, True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 120))
        screen.blit(title, title_rect)

        for button in self.buttons:
            button.draw(screen)