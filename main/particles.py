import random
import pygame
from base import Updatable


class Particle(pygame.sprite.Sprite, Updatable):
    def __init__(self, x: float, y: float, win: pygame.Surface):
        super().__init__()
        self.px = float(x)
        self.py = float(y)
        self.win = win
        self.rect = pygame.Rect(x, y, 1, 1)

    def update(self, *args, **kwargs) -> None:
        raise NotImplementedError


class Trail(Particle):
    def __init__(self, pos: tuple, color: tuple, win: pygame.Surface):
        x, y = pos
        super().__init__(x, y + 10, win)
        self.color = color
        self.vx = random.randint(0, 20) / 10 - 1
        self.vy = -2.0
        self.size = float(random.randint(4, 7))

        self.rect = pygame.draw.circle(self.win, self.color,
                                       (int(self.px), int(self.py)),
                                       int(self.size))

    def update(self, *args) -> None:
        self.px -= self.vx
        self.py -= self.vy
        self.size -= 0.1

        if self.size <= 0:
            self.kill()
            return

        self.rect = pygame.draw.circle(self.win, self.color,
                                       (int(self.px), int(self.py)),
                                       int(self.size))


class Explosion(Particle):
    def __init__(self, x: float, y: float, win: pygame.Surface):
        super().__init__(x, y, win)
        self.size = float(random.randint(4, 9))
        self.life = 40
        self.lifetime = 0
        self.x_vel = random.randrange(-4, 4)
        self.y_vel = random.randrange(-4, 4)
        self.color = 150

    def update(self, screen_scroll: int = 0) -> None:
        self.size -= 0.2
        self.lifetime += 1
        self.color = max(0, self.color - 2)

        if self.lifetime <= self.life:
            self.px += self.x_vel + screen_scroll
            self.py += self.y_vel
            s = int(self.size)
            if s > 0:
                pygame.draw.rect(self.win,
                                 (self.color, self.color, self.color),
                                 (self.px, self.py, s, s))
        else:
            self.kill()
