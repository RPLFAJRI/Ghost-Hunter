import pygame
from base import Character

WIDTH, HEIGHT = 640, 384


class Player(Character):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, size=24, speed=3, jump_height=20)

        self.grenades: int = 5
        self._attack: bool = False

        self.__idle_index: int = 0
        self.__walk_index: int = 0
        self.__attack_index: int = 0
        self.__death_index: int = 0
        self.__hit_index: int = 0

        self._load_animations()

        self.image = self.animations['idle'][self.__idle_index]
        self.rect = self.image.get_rect(center=(x, y))

    @property
    def attack(self) -> bool:
        return self._attack

    @attack.setter
    def attack(self, value: bool) -> None:
        self._attack = value

    def _load_animations(self) -> None:
        idle = self._load_frames('Player', 'PlayerIdle', 2, 24)
        walk_r, walk_l = self._load_frames('Player', 'PlayerWalk', 5, 24, flipped=True)
        attack = self._load_frames('Player', 'PlayerAttack', 4, 24)
        death = self._load_frames('Player', 'PlayerDead', 10, 24)
        hit = self._load_frames('Player', 'PlayerHit', 2, 24)

        self.animations = {
            'idle': idle,
            'walk_right': walk_r,
            'walk_left': walk_l,
            'attack': attack,
            'death': death,
            'hit': hit,
        }

    def _update_animation(self) -> None:
        self.counter += 1
        if self.counter % self.anim_speed == 0:
            if self._health <= 0:
                self.__death_index += 1
                if self.__death_index >= len(self.animations['death']):
                    self._alive = False
            else:
                if self._attack:
                    self.__attack_index += 1
                    if self.__attack_index >= len(self.animations['attack']):
                        self.__attack_index = 0
                        self._attack = False
                if self._hit:
                    self.__hit_index += 1
                    if self.__hit_index >= len(self.animations['hit']):
                        self.__hit_index = 0
                        self._hit = False
                if self._direction == 0:
                    self.__idle_index = (self.__idle_index + 1) % len(self.animations['idle'])
                elif self._direction in (-1, 1):
                    self.__walk_index = (self.__walk_index + 1) % len(self.animations['walk_left'])
            self.counter = 0

        if self._alive:
            if self._health <= 0:
                self.image = self.animations['death'][self.__death_index]
            elif self._attack:
                self.image = self.animations['attack'][self.__attack_index]
                if self._direction == -1:
                    self.image = pygame.transform.flip(self.image, True, False)
            elif self._hit:
                self.image = self.animations['hit'][self.__hit_index]
            elif self._direction == 0:
                self.image = self.animations['idle'][self.__idle_index]
            elif self._direction == -1:
                self.image = self.animations['walk_left'][self.__walk_index]
            elif self._direction == 1:
                self.image = self.animations['walk_right'][self.__walk_index]

    def _check_collision(self, world, dx: int, dy: int) -> tuple:
        for tile in world.ground_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
                if self.rect.y + dy <= tile[1].y:
                    dy = tile[1].top - self.rect.bottom

        for tile in world.rock_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.size, self.size):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.size, self.size):
                if self.vel > 0 and self.vel != self.jump_height:
                    dy = 0
                    self._jump = False
                    self.vel = self.jump_height
                elif self.vel <= 0 or self.vel == self.jump_height:
                    dy = tile[1].top - self.rect.bottom

        return dx, dy

    def update(self, moving_left: bool, moving_right: bool, world) -> None:
        self.dx = 0
        self.dy = 0

        if moving_left:
            self.dx = -self.speed
            self._direction = -1
        if moving_right:
            self.dx = self.speed
            self._direction = 1
        if not moving_left and not moving_right and not self._jump:
            self._direction = 0
            self.__walk_index = 0

        self._apply_gravity()
        self.dx, self.dy = self._check_collision(world, self.dx, self.dy)

        if self.rect.left + self.dx < 0 or self.rect.right + self.dx > WIDTH:
            self.dx = 0

        self.rect.x += self.dx
        self.rect.y += self.dy
        self._update_animation()

    def draw(self, win: pygame.Surface) -> None:
        win.blit(self.image, self.rect)
