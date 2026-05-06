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

        # self.entering_name = True
        # self.player_name = ""
        # self.saved = False
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

    # def save_score(self):
    #     if not self.saved:
    #         self.scoreboard.add_score(
    #             self.player_name,
    #             self.manager.final_time
    #         )
    #         self.saved = True
    #         self.entering_name = False

    def handle_events(self, events):
        for event in events:
            self.button.handle_event(event)

    def update(self):
        self.update_animation()
        self.button.update()

    def draw(self, screen, clock):
        screen.fill((10, 10, 18))

        center_x = screen.get_width() // 2
        screen_h = screen.get_height()

        # =========================
        # SAFE LAYOUT AREA
        # =========================
        top_y = 100 - self.slide_offset

        # dynamic safe bottom (IMPORTANT FIX)
        bottom_margin = 80
        max_button_y = screen_h - bottom_margin

        spacing = 45

        # =========================
        # TITLE
        # =========================
        title = self.font.title.render(ui.TOP_RUNS_TITLE, True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, top_y))
        screen.blit(title, title_rect)

        # spacing based on title height (clean + scalable)
        title_spacing = 45

        # =========================
        # SUBTITLE
        # =========================
        subtitle = self.font.timer.render(
            ui.TOP_RUNS_SUBTITLE,
            True,
            (160, 160, 160)
        )

        subtitle_y = top_y + title_spacing

        subtitle_rect = subtitle.get_rect(center=(center_x, subtitle_y))
        screen.blit(subtitle, subtitle_rect)

        # =========================
        # LEADERBOARD PANEL START
        # =========================
        top_scores = self.scoreboard.get_top()

        panel_start_y = top_y + 90
        line_height = 30

        # draw soft background panel (optional but huge visual improvement)
        panel_height = min(250, len(top_scores) * line_height + 40)

        panel_rect = pygame.Rect(
            center_x - 300,
            panel_start_y - 20,
            600,
            panel_height
        )

        panel = pygame.Surface(panel_rect.size)
        panel.set_alpha(120)
        panel.fill((30, 30, 45))
        screen.blit(panel, panel_rect.topleft)

        # =========================
        # SCORES
        # =========================
        for i, s in enumerate(top_scores[:8]):

            # check if this is the current run
            is_current_run = s.get("run_id") == self.manager.current_run_id

            if is_current_run:
                color = (255, 220, 120)  # highlight (gold-ish)
            else:
                color = (220, 220, 220)

            label = " (YOU)" if is_current_run else ""

            entry = self.font.timer.render(
                f"{i + 1}. {s['name']}{label} - {s['time']:.2f}s",
                True,
                color
            )

            y = panel_start_y + i * line_height
            entry_rect = entry.get_rect(center=(center_x, y))
            screen.blit(entry, entry_rect)

        # =========================
        # BUTTON
        # =========================
        button_y = min(
            panel_start_y + len(top_scores[:8]) * line_height + 60,
            max_button_y
        )

        self.button.rect.center = (center_x, button_y + self.slide_offset)
        self.button.draw(screen)

        # =========================
        # FADE
        # =========================
        fade = pygame.Surface(screen.get_size())
        fade.set_alpha(255 - self.alpha)
        fade.fill((0, 0, 0))
        screen.blit(fade, (0, 0))