import pygame
import ui_text as ui
from game.ui.button import Button
from game.states.animated_state import AnimatedState


class ScoreboardState(AnimatedState):
    def __init__(self, manager, font, screen, scoreboard):
        super().__init__()

        self.manager = manager
        self.font = font
        self.screen = screen

        self.scoreboard = scoreboard
        self.scores = self.scoreboard.get_all()

        self.scroll_offset = 0
        self.scroll_speed = 25

        center_x = screen.get_width() // 2
        bottom_y = screen.get_height() - 80

        self.back_button = Button(
            ui.BUTTON_BACK_TO_MENU,
            (center_x, bottom_y),
            (260, 55),
            font.ui_medium,
            self.go_back
        )

    def go_back(self):
        self.manager.set_state("menu")

    # =========================
    # INPUT
    # =========================
    def handle_events(self, events):
        for event in events:
            self.back_button.handle_event(event)

            # MOUSE SCROLL
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_offset += event.y * self.scroll_speed

    # =========================
    # UPDATE
    # =========================
    def update(self):
        self.update_animation()
        self.back_button.update()
        self.scores = self.scoreboard.get_all()

        # clamp scroll
        visible_height = self.screen.get_height() - 140 - 150
        content_height = len(self.scores) * 30

        max_scroll = max(0, content_height - visible_height)

        self.scroll_offset = max(-max_scroll, min(0, self.scroll_offset))

    # =========================
    # DRAW
    # =========================
    def draw(self, screen, clock):
        screen.fill((10, 10, 18))

        list_top = 150
        list_bottom = screen.get_height() - 140  # leave space for button
        list_height = list_bottom - list_top

        viewport = pygame.Rect(0, list_top, screen.get_width(), list_height)

        center_x = screen.get_width() // 2

        # -------------------------
        # TITLE
        # -------------------------
        title = self.font.title.render(ui.BUTTON_SCOREBOARD, True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, 100 - self.slide_offset))
        screen.blit(title, title_rect)

        previous_clip = screen.get_clip()
        screen.set_clip(viewport)

        # -------------------------
        # SCORE LIST
        # -------------------------
        line_height = 30
        start_y = list_top + line_height // 2 + self.scroll_offset - self.slide_offset

        for i, s in enumerate(self.scores):
            y = start_y + i * 30

            text = self.font.timer.render(
                f"{i + 1}. {s['name']} - {s['time']:.2f}s",
                True,
                (220, 220, 220)
            )

            text_rect = text.get_rect(center=(center_x, y))
            screen.blit(text, text_rect)

        # -------------------------
        # EMPTY STATE
        # -------------------------
        if not self.scores:
            empty = self.font.ui_medium.render(
                "No scores yet",
                True,
                (150, 150, 150)
            )
            rect = empty.get_rect(center=(center_x, screen.get_height() // 2))
            screen.blit(empty, rect)

        screen.set_clip(previous_clip)

        # -------------------------
        # BACK BUTTON
        # -------------------------
        self.back_button.rect.center = (
            center_x,
            screen.get_height() - 80 + self.slide_offset
        )
        self.back_button.draw(screen)

        # -------------------------
        # FADE
        # -------------------------
        fade = pygame.Surface(screen.get_size())
        fade.set_alpha(255 - self.alpha)
        fade.fill((0, 0, 0))
        screen.blit(fade, (0, 0))