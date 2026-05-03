import pygame
import ui_theme as theme


class Button:
    def __init__(self, text, center_pos, size, font, callback):
        self.text = text
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center_pos

        self.font = font
        self.callback = callback

        self.hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def update(self):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, screen):
        color = theme.BUTTON_HOVER_COLOR if self.hovered else theme.BUTTON_COLOR

        # background
        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=theme.BUTTON_RADIUS
        )

        # border
        pygame.draw.rect(
            screen,
            theme.BUTTON_BORDER_COLOR,
            self.rect,
            width=theme.BUTTON_BORDER_WIDTH,
            border_radius=theme.BUTTON_RADIUS
        )

        # text
        text_surf = self.font.render(self.text, True, theme.BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)