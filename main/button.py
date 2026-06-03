import pygame


class Button:
    def __init__(self, x: int, y: int, image: pygame.Surface,
                 scale: float, text: pygame.Surface = None,
                 xoff: int = None):
        self.width  = int(image.get_width() * scale)
        self.height = int(image.get_height() * scale)
        self.image  = pygame.transform.scale(image, (self.width, self.height))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.text = None
        if text is not None:
            self.text = text
            self.xoff = xoff if xoff is not None else text.get_width() // 2
            self.yoff = text.get_height() // 2

        self.clicked: bool = False

    def draw(self, surface: pygame.Surface) -> bool:
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        if self.text:
            self.image.blit(self.text,
                             (self.width // 2 - self.xoff,
                              self.height // 2 - self.yoff))

        return action
