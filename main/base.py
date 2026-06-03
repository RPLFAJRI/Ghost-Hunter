from abc import ABC, abstractmethod
import pygame


class Drawable(ABC):
    @abstractmethod
    def draw(self, win: pygame.Surface) -> None:
        pass


class Updatable(ABC):
    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        pass


class GameEntity(pygame.sprite.Sprite, Drawable, Updatable):
    def __init__(self, x: int, y: int, size: int):
        super().__init__()
        self.x = x
        self.y = y
        self.size = size

        self._health: int = 100
        self._alive: bool = True
        self.animations: dict = {}

        self.counter: int = 0
        self.anim_speed: int = 7

        self.image: pygame.Surface = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect: pygame.Rect = self.image.get_rect(center=(x, y))

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, value: int) -> None:
        self._health = max(0, value)
        if self._health <= 0:
            self._alive = False

    @property
    def alive(self) -> bool:
        return self._alive

    @alive.setter
    def alive(self, value: bool) -> None:
        self._alive = value

    @abstractmethod
    def _load_animations(self) -> None:
        pass

    @abstractmethod
    def _update_animation(self) -> None:
        pass

    def _load_frames(self, folder: str, prefix: str,
                     count: int, size: int, flipped: bool = False):
        right_frames = []
        left_frames = []
        for i in range(1, count + 1):
            img = pygame.image.load(f'Assets/{folder}/{prefix}{i}.png')
            img = pygame.transform.scale(img, (size, size))
            right_frames.append(img)
            if flipped:
                left_frames.append(pygame.transform.flip(img, True, False))
        if flipped:
            return right_frames, left_frames
        return right_frames

    def draw(self, win: pygame.Surface) -> None:
        win.blit(self.image, self.rect)


class Character(GameEntity):
    def __init__(self, x: int, y: int, size: int,
                 speed: int = 3, jump_height: int = 15):
        super().__init__(x, y, size)

        self._hit: bool = False
        self._direction: int = 0

        self.speed = speed
        self.jump_height = jump_height
        self.vel = jump_height
        self.mass = 1
        self.gravity = 1
        self._jump: bool = False

        self.dx: int = 0
        self.dy: int = 0

    @property
    def hit(self) -> bool:
        return self._hit

    @hit.setter
    def hit(self, value: bool) -> None:
        self._hit = value

    @property
    def direction(self) -> int:
        return self._direction

    @property
    def jump(self) -> bool:
        return self._jump

    @jump.setter
    def jump(self, value: bool) -> None:
        self._jump = value

    def _apply_gravity(self) -> None:
        if self._jump:
            F = (1 / 2) * self.mass * self.vel
            self.dy -= F
            self.vel -= self.gravity
            if self.vel < -15:
                self.vel = self.jump_height
                self._jump = False
        else:
            self.dy += self.vel


class WorldObject(pygame.sprite.Sprite, Updatable):
    def __init__(self, x: int, y: int, tile_data: tuple):
        super().__init__()
        self.image = tile_data[0]
        self.rect = tile_data[1].copy()
        self.rect.x = x
        self.rect.y = y
        self.origin_x = x

    def update(self, screen_scroll: int) -> None:
        self.rect.x += screen_scroll

    def draw(self, win: pygame.Surface) -> None:
        win.blit(self.image, self.rect)


class Projectile(pygame.sprite.Sprite, Drawable, Updatable):
    def __init__(self, x: int, y: int, direction: int, win: pygame.Surface):
        super().__init__()
        self.px = float(x)
        self.py = float(y)
        self.direction = direction
        self.win = win
        self.radius = 4
        self.rect = pygame.Rect(x, y, self.radius * 2, self.radius * 2)

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        pass

    def draw(self, win: pygame.Surface) -> None:
        pass
