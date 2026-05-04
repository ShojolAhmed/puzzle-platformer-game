import pygame
import ui_theme as theme
import ui_text as ui
from game.ui.button import Button
from game.states.animated_state import AnimatedState

class GameCompletedState(AnimatedState):
    def __init__(self, manager, font, screen, scoreboard):
        super().__init__()

        self.manager = manager
        self.font = font
        self.screen = screen

        self.entering_name = True
        self.player_name = ""
        self.saved = False
        self.scoreboard = scoreboard

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

    def save_score(self):
        if not self.saved:
            self.scoreboard.add_score(
                self.player_name,
                self.manager.final_time
            )
            self.saved = True
            self.entering_name = False

    def handle_events(self, events):
        for event in events:
            self.button.handle_event(event)

            if self.entering_name:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_RETURN and self.player_name:
                        self.save_score()

                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]

                    else:
                        if len(self.player_name) < 12 and event.unicode.isprintable():
                            self.player_name += event.unicode

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



        top_scores = self.scoreboard.get_top()

        # -------------------------
        # NAME INPUT
        # -------------------------
        if self.entering_name:
            prompt = self.font.ui_medium.render(
                "Enter Name: " + self.player_name,
                True,
                (255, 255, 255)
            )
            screen.blit(prompt, (center_x - 120, center_y + 30))

        else:
            # -------------------------
            # TOP N LEADERBOARD
            # -------------------------
            y_offset = 40
            title = self.font.ui_medium.render("Top Runs", True, (255, 255, 255))
            screen.blit(title, (center_x - 60, center_y + 40))

            for i, s in enumerate(top_scores):
                text = self.font.timer.render(
                    f"{i + 1}. {s['name']} - {s['time']:.2f}s",
                    True,
                    (200, 200, 200)
                )
                screen.blit(text, (center_x - 100, center_y + 80 + i * 25))