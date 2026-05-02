import pygame


class Button:
    def __init__(self, text, center_pos, size, font, callback):
        self.text = text
        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center_pos  # ← center positioning
        self.font = font
        self.callback = callback

        self.base_color = (70, 70, 70)
        self.hover_color = (120, 120, 120)
        self.text_color = (255, 255, 255)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color

        pygame.draw.rect(screen, color, self.rect, border_radius=8)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)

        screen.blit(text_surf, text_rect)