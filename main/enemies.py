import random
import pygame
from base import Character
from projectiles import Bullet

TILE_SIZE = 16

pygame.mixer.init()
bullet_fx = pygame.mixer.Sound('Sounds/ghost_shot.mp3')


class Enemy(Character):
    def __init__(self, x: int, y: int, size: int,
                 patrol_range: int = 2 * TILE_SIZE,
                 shoot_range: int = 200,
                 shoot_interval: int = 50):
        super().__init__(x, y, size)

        self.initial_x = x
        self.patrol_range = patrol_range
        self.shoot_range = shoot_range
        self.shoot_interval = shoot_interval

        self.on_death_bed: bool = False
        self.shoot_timer: int = 0

        self._direction = random.choice([-1, 1])

    def _shoot(self, bullet_group: pygame.sprite.Group,
               player, win: pygame.Surface) -> None:
        raise NotImplementedError(f"{type(self).__name__} belum implementasi _shoot()")

    def _patrol(self, screen_scroll: int) -> None:
        if self._health > 0:
            self.rect.x += self._direction + screen_scroll
            self.x += screen_scroll
            if abs(self.rect.x - self.x) >= self.patrol_range:
                self._direction *= -1

    def _handle_death_transition(self) -> None:
        if self._health <= 0:
            self.on_death_bed = True


class Ghost(Enemy):
    def __init__(self, x: int, y: int, win: pygame.Surface):
        super().__init__(x, y, size=32)
        self.win = win

        self.__walk_index: int = 0
        self.__death_index: int = 0
        self.__hit_index: int = 0

        self.anim_speed = 5

        self._load_animations()
        self.image = self.animations['walk_right'][self.__walk_index]
        self.rect = self.image.get_rect(center=(x, y))

    def _load_animations(self) -> None:
        walk_r, walk_l = self._load_frames('Ghost', 'Enemywalk', 5, 32, flipped=True)
        hit = self._load_frames('Ghost', 'Enemyhit', 2, 32)
        death = self._load_frames('Ghost', 'Enemydead', 8, 32)

        self.animations = {
            'walk_right': walk_r,
            'walk_left': walk_l,
            'hit': hit,
            'death': death,
        }

    def _update_animation(self) -> None:
        self.counter += 1
        if self.counter % self.anim_speed == 0:
            if self.on_death_bed:
                self.__death_index += 1
                if self.__death_index >= len(self.animations['death']):
                    self.kill()
                    self._alive = False
            if self._hit:
                self.__hit_index += 1
                if self.__hit_index >= len(self.animations['hit']):
                    self.__hit_index = 0
                    self._hit = False
            else:
                self.__walk_index = (self.__walk_index + 1) % len(self.animations['walk_left'])

        if self._alive:
            if self.on_death_bed:
                self.image = self.animations['death'][self.__death_index]
            elif self._hit:
                self.image = self.animations['hit'][self.__hit_index]
            else:
                if self._direction == -1:
                    self.image = self.animations['walk_left'][self.__walk_index]
                else:
                    self.image = self.animations['walk_right'][self.__walk_index]

    def _shoot(self, bullet_group: pygame.sprite.Group,
               player, win: pygame.Surface) -> None:
        if self._health > 0 and abs(player.rect.x - self.rect.x) <= self.shoot_range:
            x, y = self.rect.center
            from projectiles import Bullet
            bullet = Bullet(x, y, self._direction, (160, 160, 160), 2, win)
            bullet_group.add(bullet)
            bullet_fx.play()

    def update(self, screen_scroll: int,
               bullet_group: pygame.sprite.Group, player) -> None:
        self._patrol(screen_scroll)
        self._handle_death_transition()
        self._update_animation()

        self.counter += 1
        if self.counter % self.shoot_interval == 0:
            self._shoot(bullet_group, player, self.win)
