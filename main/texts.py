import pygame

WIDTH, HEIGHT = 640, 384


class Text:
    def __init__(self, font: str, font_size: int):
        self.font = pygame.font.Font(font, font_size)

    def render(self, text: str, color: tuple) -> pygame.Surface:
        return self.font.render(text, False, color)


class Message:
    def __init__(self, x: int, y: int, size: int,
                 text: str, font, color: tuple, win: pygame.Surface):
        self.win   = win
        self.color = color
        self.x, self.y = x, y

        if not font:
            self.font = pygame.font.SysFont("Verdana", size)
            anti_alias = True
        else:
            self.font = pygame.font.Font(font, size)
            anti_alias = False

        self.anti_alias = anti_alias
        self.image = self.font.render(text, anti_alias, color)
        self.rect  = self.image.get_rect(center=(x, y))

        self.shadow_color = (255, 255, 255) if color == (200, 200, 200) else (54, 69, 79)
        self.shadow      = self.font.render(text, anti_alias, self.shadow_color)
        self.shadow_rect = self.image.get_rect(center=(x + 2, y + 2))

    def update(self, text: str = None, color: tuple = None, shadow: bool = True) -> None:
        if text:
            c = color if color else self.color
            self.image = self.font.render(str(text), self.anti_alias, c)
            self.rect  = self.image.get_rect(center=(self.x, self.y))
            self.shadow = self.font.render(str(text), self.anti_alias, self.shadow_color)
            self.shadow_rect = self.image.get_rect(center=(self.x + 2, self.y + 2))

        if shadow:
            self.win.blit(self.shadow, self.shadow_rect)
        self.win.blit(self.image, self.rect)


class BlinkingText(Message):
    def __init__(self, x: int, y: int, size: int,
                 text: str, font, color: tuple, win: pygame.Surface):
        super().__init__(x, y, size, text, font, color, win)
        self.index: int  = 0
        self.show: bool  = True

    def update(self, *args, **kwargs) -> None:
        self.index += 1
        if self.index % 40 == 0:
            self.show = not self.show

        if self.show:
            self.win.blit(self.image, self.rect)


def MessageBox(win: pygame.Surface, font: pygame.font.Font,
               name: str, text: str) -> None:
    BOX_W, BOX_H = WIDTH - 40, HEIGHT - 84
    x, y = 35, 65

    pygame.draw.rect(win, (255, 255, 255), (25, 25, BOX_W, BOX_H), border_radius=10)

    # Split text by '||' for forced line breaks, then wrap words
    segments = text.split('||')
    for segment in segments:
        words = segment.strip().split(' ')
        for word in words:
            if not word:
                continue
            rendered = font.render(word, True, (0, 0, 0))
            if x + rendered.get_width() >= WIDTH - 20:
                x = 35
                y += 25
            win.blit(rendered, (x, y))
            x += rendered.get_width() + 5
        # Force newline after each segment
        x = 35
        y += 30

    title       = font.render(name, True, (0, 0, 0))
    title_width = 120
    pygame.draw.rect(win, (255, 255, 255),
                     (WIDTH // 2 - title_width // 2 + 10, 10, title_width, 30),
                     border_radius=10)
    win.blit(title, (WIDTH // 2 - title.get_width() // 2 + 10, 10))
