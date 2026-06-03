import math
import pygame
from base import Projectile
from particles import Explosion

WIDTH, HEIGHT = 640, 384

pygame.mixer.init()
grenade_blast_fx = pygame.mixer.Sound('Sounds/grenade blast.wav')
grenade_blast_fx.set_volume(0.6)


class Bullet(Projectile):
    def __init__(self, x: int, y: int, direction: int,
                 color: tuple, type_: int, win: pygame.Surface):
        super().__init__(x, y, direction, win)
        self.color = color
        self.speed = 10
        self.bullet_type = type_

        self.rect = pygame.draw.circle(self.win, self.color,
                                       (int(self.px), int(self.py)),
                                       self.radius)

    @property
    def type(self) -> int:
        return self.bullet_type

    def update(self, screen_scroll: int, world) -> None:
        if self.direction == -1:
            self.px -= self.speed + screen_scroll
        else:
            self.px += self.speed + screen_scroll

        for tile in world.ground_list:
            if tile[1].collidepoint(self.px, self.py):
                self.kill()
                return
        for tile in world.rock_list:
            if tile[1].collidepoint(self.px, self.py):
                self.kill()
                return

        self.rect = pygame.draw.circle(self.win, self.color,
                                       (int(self.px), int(self.py)),
                                       self.radius)

    def draw(self, win: pygame.Surface) -> None:
        pass


class Grenade(Projectile):
    DMG_FAR    = 20
    DMG_MID    = 50
    DMG_CLOSE  = 80
    ENEMY_DMG  = 100
    BLAST_RADIUS = 100

    def __init__(self, x: int, y: int, direction: int, win: pygame.Surface):
        super().__init__(x, y, direction, win)
        self.speed: float = 10.0
        self.vel_y: float = -11.0
        self.timer: int = 15

        if self.direction == 0:
            self.direction = 1

        self._draw_grenade()

    def _draw_grenade(self) -> None:
        pygame.draw.circle(self.win, (200, 200, 200),
                           (int(self.px), int(self.py)), self.radius + 1)
        self.rect = pygame.draw.circle(self.win, (255, 50, 50),
                                       (int(self.px), int(self.py)), self.radius)
        pygame.draw.circle(self.win, (0, 0, 0),
                           (int(self.px), int(self.py)), 1)

    def _calculate_damage(self, distance: float) -> int:
        if distance > 80:
            return self.DMG_FAR
        elif distance > 40:
            return self.DMG_MID
        return self.DMG_CLOSE

    def _explode(self, player, enemy_group: pygame.sprite.Group,
                  explosion_group: pygame.sprite.Group) -> None:
        grenade_blast_fx.play()

        for _ in range(30):
            explosion_group.add(Explosion(self.px, self.py, self.win))

        p_dist = math.hypot(player.rect.centerx - self.px,
                            player.rect.centery - self.py)
        if p_dist <= self.BLAST_RADIUS:
            player.health -= self._calculate_damage(p_dist)
            player.hit = True

        for enemy in enemy_group:
            e_dist = math.hypot(enemy.rect.centerx - self.px,
                                enemy.rect.centery - self.py)
            if e_dist < 80:
                enemy.health -= self.ENEMY_DMG

        self.kill()

    def update(self, screen_scroll: int, player,
               enemy_group: pygame.sprite.Group,
               explosion_group: pygame.sprite.Group,
               world) -> None:
        self.vel_y += 1
        dx = self.direction * self.speed
        dy = self.vel_y

        for tile in world.ground_list:
            if tile[1].colliderect(self.rect.x, self.rect.y,
                                   self.rect.width, self.rect.height):
                if self.rect.y <= tile[1].y:
                    dy = 0
                    self.speed = max(0.0, self.speed - 1)

        for tile in world.rock_list:
            if tile[1].colliderect(self.rect.x + dx, self.rect.y,
                                   self.rect.width, self.rect.height):
                self.direction *= -1
                dx = self.direction * self.speed
            if tile[1].colliderect(self.rect.x, self.rect.y + dy,
                                   self.rect.width, self.rect.height):
                if self.rect.y <= tile[1].y:
                    dy = 0
                    self.speed = max(0.0, self.speed - 1)

        if self.rect.y > WIDTH:
            self.kill()
            return

        if self.speed == 0:
            self.timer -= 1
            if self.timer <= 0:
                self._explode(player, enemy_group, explosion_group)
                return

        self.px += dx + screen_scroll
        self.py += dy
        self._draw_grenade()

    def draw(self, win: pygame.Surface) -> None:
        pass
