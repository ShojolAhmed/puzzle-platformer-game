import pygame
import ui_theme as theme
import ui_text as ui
from game.ui.button import Button
from game.states.animated_state import AnimatedState

class MenuState(AnimatedState):
    def __init__(self, manager, font, screen):
        super().__init__()

        self.manager = manager
        self.font = font
        self.screen = screen

        self.buttons = []
        self.build_buttons()

    def build_buttons(self):
        self.buttons = []

        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2

        button_w = 260
        button_h = 55
        spacing = 20

        options = []

        if self.manager.has_active_game():
            options.append(("continue", self.continue_game))

        options += [
            ("start", self.start_game),
            ("scoreboard", self.scoreboard),
            ("quit", self.quit_game),
        ]

        total_height = len(options) * button_h + (len(options) - 1) * spacing

        start_y = center_y - total_height // 2

        for i, (text_key, callback) in enumerate(options):
            y = start_y + i * (button_h + spacing)

            import ui_text as ui

            text_map = {
                "continue": ui.BUTTON_CONTINUE,
                "start": ui.BUTTON_START,
                "scoreboard": ui.BUTTON_SCOREBOARD,
                "quit": ui.BUTTON_QUIT,
            }

            self.buttons.append(
                Button(
                    text_map[text_key],
                    (center_x, y + button_h // 2),
                    (button_w, button_h),
                    self.font.ui_medium,
                    callback
                )
            )

    def start_game(self):
        self.manager.start_new_run()
        play = self.manager.states["play"]()
        self.manager.set_play_state(play)

    def continue_game(self):
        play = self.manager.play_state
        play.timer.start()  # resume timer
        self.manager.continue_game()

    def scoreboard(self):
        self.manager.set_state("scoreboard")

    def quit_game(self):
        pygame.quit()
        exit()

    def handle_events(self, events):
        for event in events:
            for button in self.buttons:
                button.handle_event(event)

    def update(self):
        # fade in
        if self.alpha < 255:
            self.alpha += self.anim_speed

        # slide in
        if self.slide_offset > 0:
            self.slide_offset -= 2

        for button in self.buttons:
            button.update()

    def draw(self, screen, clock):
        screen.fill((10, 10, 18))

        center_x = screen.get_width() // 2

        # ---------- TITLE ----------
        title = self.font.title.render(ui.MENU_TITLE, True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, 120 - self.slide_offset))
        screen.blit(title, title_rect)

        # ---------- SUBTITLE ----------
        subtitle_font = pygame.font.Font(None, 28)
        subtitle = subtitle_font.render(
            "Press ESC in-game to return here",
            True,
            (160, 160, 160)
        )
        subtitle_rect = subtitle.get_rect(center=(center_x, 170 - self.slide_offset))
        screen.blit(subtitle, subtitle_rect)

        # ---------- BUTTON AREA START (IMPORTANT FIX) ----------
        start_y = 260  # 👈 reserved space below title/subtitle

        # reposition button block safely
        spacing = 75
        button_height = 55

        total_height = len(self.buttons) * button_height + (len(self.buttons) - 1) * (spacing - button_height)
        start_y = (screen.get_height() // 2) - total_height // 2 + 80  # push lower than title

        for i, button in enumerate(self.buttons):
            target_y = start_y + i * spacing + self.slide_offset

            button.rect.center = (center_x, target_y)
            button.draw(screen)

        # ---------- FADE ----------
        fade = pygame.Surface(screen.get_size())
        fade.set_alpha(255 - self.alpha)
        fade.fill((0, 0, 0))
        screen.blit(fade, (0, 0))