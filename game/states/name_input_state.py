import pygame
import ui_text as ui
from game.states.animated_state import AnimatedState


class NameInputState(AnimatedState):
    def __init__(self, manager, font, screen, scoreboard):
        super().__init__()

        self.manager = manager
        self.font = font
        self.screen = screen

        self.name = ""
        self.max_length = 12
        self.cursor_timer = 0

        self.scoreboard = scoreboard
        self.final_time = manager.final_time

    # =========================
    # INPUT
    # =========================
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN and self.name:
                    self.save_and_continue()

                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]

                else:
                    if len(self.name) < self.max_length and event.unicode.isprintable():
                        self.name += event.unicode

    # =========================
    # SAVE + NEXT
    # =========================
    def save_and_continue(self):
        self.scoreboard.add_score(
            self.name,
            self.final_time,
            self.manager.current_run_id
        )
        self.manager.set_state("game_completed")

    # =========================
    # UPDATE
    # =========================
    def update(self):
        self.update_animation()
        self.cursor_timer += 1

    # =========================
    # DRAW
    # =========================
    def draw(self, screen, clock):
        screen.fill((10, 10, 18))

        title_gap = 0
        time_gap = 40
        input_gap = 50
        hint_gap = 30

        total_height = (
                60 +  # title approx height
                time_gap +
                50 +  # time approx height
                input_gap +
                50 +  # input box height
                hint_gap +
                20  # hint height
        )

        center_x = screen.get_width() // 2

        # =========================
        # LAYOUT (CLEAN)
        # =========================
        center_y = screen.get_height() // 2
        start_y = center_y - total_height // 2 - self.slide_offset



        # =========================
        # TITLE (BIG)
        # =========================
        title_y = start_y

        title = self.font.title.render(ui.GAME_COMPLETED_TITLE, True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, title_y))
        screen.blit(title, title_rect)

        # =========================
        # TIME (HIGHLIGHTED)
        # =========================
        t = self.final_time

        minutes = int(t // 60)
        seconds = int(t % 60)
        ms = int((t - int(t)) * 100)

        time_y = title_y + 60 + time_gap

        time_text = self.font.timer.render(
            f"Time: {minutes:02}:{seconds:02}.{ms:02}",
            True,
            (255, 220, 120)
        )

        time_rect = time_text.get_rect(center=(center_x, time_y))
        screen.blit(time_text, time_rect)

        glow = self.font.timer.render(
            f"Time: {minutes:02}:{seconds:02}.{ms:02}",
            True,
            (255, 180, 80)
        )

        glow_rect = glow.get_rect(center=(center_x, time_y + 2))
        screen.blit(glow, glow_rect)

        # =========================
        # INPUT BOX BACKGROUND
        # =========================
        input_y = time_y + 50 + input_gap

        box_width = 320
        box_height = 50

        box_rect = pygame.Rect(0, 0, box_width, box_height)
        box_rect.center = (center_x, input_y)

        # background
        pygame.draw.rect(screen, (25, 25, 35), box_rect, border_radius=8)

        # border
        pygame.draw.rect(screen, (80, 80, 120), box_rect, 2, border_radius=8)

        show_cursor = (self.cursor_timer // 30) % 2 == 0

        # =========================
        # NAME TEXT
        # =========================
        if self.name:
            display_name = self.name + ("|" if show_cursor else "")
        else:
            display_name = ui.ENTER_NAME

        color = (255, 255, 255) if self.name else (120, 120, 120)

        name_text = self.font.ui_medium.render(display_name, True, color)
        name_rect = name_text.get_rect(center=box_rect.center)

        screen.blit(name_text, name_rect)

        # =========================
        # HINT
        # =========================
        hint = self.font.timer.render(
            ui.NAME_CONFIRM,
            True,
            (160, 160, 160)
        )

        hint_y = input_y + 50 + hint_gap

        hint_rect = hint.get_rect(center=(center_x, hint_y))
        screen.blit(hint, hint_rect)

        # =========================
        # FADE
        # =========================
        fade = pygame.Surface(screen.get_size())
        fade.set_alpha(255 - self.alpha)
        fade.fill((0, 0, 0))
        screen.blit(fade, (0, 0))