import pygame

from world import World, load_level
from player import Player
from enemies import Ghost
from particles import Trail
from projectiles import Bullet, Grenade
from button import Button
from texts import Text, Message, BlinkingText, MessageBox


class GameManager:
    WIDTH, HEIGHT = 640, 384
    TILE_SIZE     = 16
    FPS           = 45
    SCROLL_THRES  = 200
    MAX_LEVEL     = 3
    ROWS, COLS    = 24, 40

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT), pygame.NOFRAME
        )
        self.clock = pygame.time.Clock()

        self.level: int         = 1
        self.level_length: int  = 0
        self.screen_scroll: int = 0
        self.bg_scroll: int     = 0
        self.dx: int            = 0

        self.main_menu: bool    = True
        self.about_page: bool   = False
        self.controls_page: bool= False
        self.game_start: bool   = False
        self.game_won: bool     = True
        self.running: bool      = True

        self.moving_left: bool  = False
        self.moving_right: bool = False

        self.world  = None
        self.player = None

        self._load_assets()
        self._create_groups()
        self._create_ui()
        self._load_audio()
        self._init_menu_decoration()

    def _load_assets(self) -> None:
        W, H = self.WIDTH, self.HEIGHT
        self.BG1  = pygame.transform.scale(pygame.image.load('assets/BG1.png'), (W, H))
        self.BG2  = pygame.transform.scale(pygame.image.load('assets/BG2.png'), (W, H))
        self.BG3  = pygame.transform.scale(pygame.image.load('assets/BG3.png'), (W, H))
        self.MOON = pygame.transform.scale(pygame.image.load('assets/moon.png'), (300, 220))

    def _create_groups(self) -> None:
        self.trail_group     = pygame.sprite.Group()
        self.bullet_group    = pygame.sprite.Group()
        self.grenade_group   = pygame.sprite.Group()
        self.explosion_group = pygame.sprite.Group()
        self.enemy_group     = pygame.sprite.Group()
        self.water_group     = pygame.sprite.Group()
        self.diamond_group   = pygame.sprite.Group()
        self.potion_group    = pygame.sprite.Group()
        self.exit_group      = pygame.sprite.Group()

        self.objects_group = [
            self.water_group,
            self.diamond_group,
            self.potion_group,
            self.enemy_group,
            self.exit_group,
        ]

    def _create_ui(self) -> None:
        title_font        = "Fonts/Aladin-Regular.ttf"
        instructions_font = 'Fonts/BubblegumSans-Regular.ttf'

        self.ghostbusters  = Message(self.WIDTH//2+50, self.HEIGHT//2-90, 90,
                                      "Ghost Hunter", title_font, (255,255,255), self.win)
        self.left_key      = Message(self.WIDTH//2+10, self.HEIGHT//2-90, 20,
                                      "Press left a to go left",
                                      instructions_font, (255,255,255), self.win)
        self.right_key     = Message(self.WIDTH//2+10, self.HEIGHT//2-65, 20,
                                      "Press right d to go right",
                                      instructions_font, (255,255,255), self.win)
        self.up_key        = Message(self.WIDTH//2+10, self.HEIGHT//2-45, 20,
                                      "Press up w to jump",
                                      instructions_font, (255,255,255), self.win)
        self.space_key     = Message(self.WIDTH//2+10, self.HEIGHT//2-25, 20,
                                      "Press space key to shoot",
                                      instructions_font, (255,255,255), self.win)
        self.g_key         = Message(self.WIDTH//2+10, self.HEIGHT//2-5, 20,
                                      "Press g key to throw grenade",
                                      instructions_font, (255,255,255), self.win)
        self.game_won_msg  = Message(self.WIDTH//2+10, self.HEIGHT//2-5, 20,
                                      "You have won the game",
                                      instructions_font, (255,255,255), self.win)

        t = Text(instructions_font, 18)
        fc = (12, 12, 12)
        play_surf     = t.render('Play', fc)
        about_surf    = t.render('About', fc)
        controls_surf = t.render('Controls', fc)
        exit_surf     = t.render('Exit', fc)
        menu_surf     = t.render('Main Menu', fc)

        self.about_font = pygame.font.SysFont('Times New Roman', 20)

        self.about_info = (
            "ini adalah game aksi 2D di mana pemain melawan musuh "
            "yang muncul di berbagai level. Gunakan senjata dan granat untuk mengalahkan "
            "semua musuh dan capai garis akhir! "
            " "
            "|| Team Members: "
            "||1. Fajriandi Ramadhan : Developer  "
            "||2. M Afiffudin Zain : Developer  "
            "||3. Ibrahim Al Albany : Developer  "
            "||4. Felix Nathaniel NP : Developer"
        )

        btn_bg  = pygame.image.load('Assets/ButtonBG.png')
        bw      = btn_bg.get_width()
        bx      = self.WIDTH//2 - bw//4

        self.play_btn      = Button(bx, self.HEIGHT//2,       btn_bg, 0.5, play_surf,  10)
        self.about_btn     = Button(bx, self.HEIGHT//2+35,    btn_bg, 0.5, about_surf, 10)
        self.controls_btn  = Button(bx, self.HEIGHT//2+70,    btn_bg, 0.5, controls_surf, 10)
        self.exit_btn      = Button(bx, self.HEIGHT//2+105,   btn_bg, 0.5, exit_surf,  10)
        self.main_menu_btn = Button(bx, self.HEIGHT//2+130,   btn_bg, 0.5, menu_surf,  20)

    def _load_audio(self) -> None:
        pygame.mixer.music.load('Sounds/mixkit-complex-desire-1093.mp3')
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.5)

        self.diamond_fx      = pygame.mixer.Sound('Sounds/point.mp3')
        self.diamond_fx.set_volume(0.6)
        self.bullet_fx       = pygame.mixer.Sound('Sounds/bullet.wav')
        self.jump_fx         = pygame.mixer.Sound('Sounds/jump.mp3')
        self.health_fx       = pygame.mixer.Sound('Sounds/health.wav')
        self.menu_click_fx   = pygame.mixer.Sound('Sounds/menu.mp3')
        self.next_level_fx   = pygame.mixer.Sound('Sounds/level.mp3')
        self.grenade_throw_fx= pygame.mixer.Sound('Sounds/grenade throw.wav')
        self.grenade_throw_fx.set_volume(0.6)

    def _init_menu_decoration(self) -> None:
        p_img = pygame.transform.scale(
            pygame.image.load('Assets/Player/PlayerIdle1.png'), (32, 32))
        self.p_image = p_img
        self.p_rect  = p_img.get_rect(center=(470, 200))
        self.p_dy    = 1
        self.p_ctr   = 1

    def _reset_groups(self) -> None:
        for grp in (self.trail_group, self.bullet_group, self.grenade_group,
                    self.explosion_group, self.enemy_group, self.water_group,
                    self.diamond_group, self.potion_group, self.exit_group):
            grp.empty()

    def _reset_level(self) -> None:
        self._reset_groups()
        world_data, self.level_length = load_level(self.level)
        self.world = World(self.objects_group)
        self.world.generate_world(world_data, self.win)

    def _reset_player(self) -> None:
        self.player      = Player(250, 50)
        self.moving_left = False
        self.moving_right= False

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._handle_keydown(1)

            if event.type == pygame.KEYUP:
                self._handle_keyup(event.key)

    def _handle_keydown(self, key: int) -> None:
        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False

        if key == pygame.K_a:
            self.moving_left = True
        if key == pygame.K_d:
            self.moving_right = True

        if key == pygame.K_w and self.player and not self.player.jump:
            self.player.jump = True
            self.jump_fx.play()

        if key == 1 and self.player:
            x, y = self.player.rect.center
            bullet = Bullet(x, y, self.player.direction,
                            (240, 240, 240), 1, self.win)
            self.bullet_group.add(bullet)
            self.bullet_fx.play()
            self.player.attack = True

        if key == pygame.K_g and self.player and self.player.grenades:
            self.player.grenades -= 1
            grenade = Grenade(self.player.rect.centerx,
                              self.player.rect.centery,
                              self.player.direction, self.win)
            self.grenade_group.add(grenade)
            self.grenade_throw_fx.play()

    def _handle_keyup(self, key: int) -> None:
        if key == pygame.K_a:
            self.moving_left = False
        if key == pygame.K_d:
            self.moving_right = False

    def _update_game(self) -> None:
        p = self.player
        w = self.world

        self.bullet_group.update(self.screen_scroll, w)
        self.grenade_group.update(self.screen_scroll, p,
                                   self.enemy_group, self.explosion_group, w)
        self.explosion_group.update(self.screen_scroll)
        self.trail_group.update()
        self.water_group.update(self.screen_scroll)
        self.diamond_group.update(self.screen_scroll)
        self.potion_group.update(self.screen_scroll)
        self.exit_group.update(self.screen_scroll)
        self.enemy_group.update(self.screen_scroll, self.bullet_group, p)

        if p.jump:
            self.trail_group.add(Trail(p.rect.center, (220, 220, 220), self.win))

        self.screen_scroll = 0
        p.update(self.moving_left, self.moving_right, w)

        if ((p.rect.right >= self.WIDTH - self.SCROLL_THRES
             and self.bg_scroll < (self.level_length * self.TILE_SIZE) - self.WIDTH)
                or (p.rect.left <= self.SCROLL_THRES and self.bg_scroll > abs(self.dx))):
            self.dx = p.dx
            p.rect.x -= self.dx
            self.screen_scroll = -self.dx
            self.bg_scroll    -= self.screen_scroll

        self._handle_collisions()

    def _handle_collisions(self) -> None:
        p = self.player

        if p.rect.bottom > self.HEIGHT:
            p.health = 0

        if pygame.sprite.spritecollide(p, self.water_group, False):
            p.health = 0
            self.level = 1

        if pygame.sprite.spritecollide(p, self.diamond_group, True):
            self.diamond_fx.play()

        if pygame.sprite.spritecollide(p, self.exit_group, False):
            self.next_level_fx.play()
            self.level += 1
            if self.level <= self.MAX_LEVEL:
                saved_health = p.health
                self._reset_level()
                self._reset_player()
                self.player.health = saved_health
                self.screen_scroll = 0
                self.bg_scroll     = 0
            else:
                self.game_won = True

        potions = pygame.sprite.spritecollide(p, self.potion_group, False)
        if potions and p.health < 100:
            potions[0].kill()
            p.health = min(100, p.health + 15)
            self.health_fx.play()

        for bullet in self.bullet_group:
            enemies = pygame.sprite.spritecollide(bullet, self.enemy_group, False)
            if enemies and bullet.type == 1:
                enemy = enemies[0]
                if not enemy.hit:
                    enemy.hit = True
                    enemy.health -= 50
                bullet.kill()
            if bullet.rect.colliderect(p) and bullet.type == 2:
                if not p.hit:
                    p.hit = True
                    p.health -= 20
                bullet.kill()

        if p.health <= 0:
            self._reset_level()
            self._reset_player()
            self.screen_scroll = 0
            self.bg_scroll     = 0
            self.main_menu     = True
            self.about_page    = False
            self.controls_page = False
            self.game_start    = False

    def _draw_background(self) -> None:
        self.win.fill((0, 0, 0))
        for x in range(5):
            self.win.blit(self.BG1, (x * self.WIDTH - self.bg_scroll * 0.6, 0))
            self.win.blit(self.BG2, (x * self.WIDTH - self.bg_scroll * 0.7, 0))
            self.win.blit(self.BG3, (x * self.WIDTH - self.bg_scroll * 0.8, 0))

    def _draw_menu(self) -> None:
        self.ghostbusters.update()
        self.trail_group.update()
        self.win.blit(self.p_image, self.p_rect)

        self.p_rect.y += self.p_dy
        self.p_ctr    += self.p_dy
        if self.p_ctr > 15 or self.p_ctr < -15:
            self.p_dy *= -1
        self.trail_group.add(Trail(self.p_rect.center, (220, 220, 220), self.win))

        if self.play_btn.draw(self.win):
            self.menu_click_fx.play()
            self._reset_level()
            self._reset_player()
            self.game_start    = True
            self.main_menu     = False
            self.game_won      = False

        if self.about_btn.draw(self.win):
            self.menu_click_fx.play()
            self.about_page    = True
            self.main_menu     = False

        if self.controls_btn.draw(self.win):
            self.menu_click_fx.play()
            self.controls_page = True
            self.main_menu     = False

        if self.exit_btn.draw(self.win):
            self.menu_click_fx.play()
            self.running = False

    def _draw_about(self) -> None:
        MessageBox(self.win, self.about_font, 'Ghost Hunter', self.about_info)
        if self.main_menu_btn.draw(self.win):
            self.menu_click_fx.play()
            self.about_page = False
            self.main_menu  = True

    def _draw_controls(self) -> None:
        self.left_key.update()
        self.right_key.update()
        self.up_key.update()
        self.space_key.update()
        self.g_key.update()

        if self.main_menu_btn.draw(self.win):
            self.menu_click_fx.play()
            self.controls_page = False
            self.main_menu     = True

    def _draw_won(self) -> None:
        self.game_won_msg.update()
        if self.main_menu_btn.draw(self.win):
            self.menu_click_fx.play()
            self.controls_page = False
            self.main_menu     = True
            self.level         = 1

    def _draw_game(self) -> None:
        p = self.player
        self.win.blit(self.MOON, (-40, -10))
        self.world.draw_world(self.win, self.screen_scroll)

        self.water_group.draw(self.win)
        self.diamond_group.draw(self.win)
        self.potion_group.draw(self.win)
        self.exit_group.draw(self.win)
        self.enemy_group.draw(self.win)

        p.draw(self.win)

        if p.alive:
            color = (0, 255, 0) if p.health > 40 else (255, 0, 0)
            pygame.draw.rect(self.win, color, (6, 8, p.health, 20), border_radius=10)
        pygame.draw.rect(self.win, (255, 255, 255), (6, 8, 100, 20), 2, border_radius=10)

        for i in range(p.grenades):
            pygame.draw.circle(self.win, (200, 200, 200), (20 + 15 * i, 40), 5)
            pygame.draw.circle(self.win, (255, 50, 50),   (20 + 15 * i, 40), 4)
            pygame.draw.circle(self.win, (0, 0, 0),       (20 + 15 * i, 40), 1)

    def _draw(self) -> None:
        self._draw_background()

        if not self.game_start:
            self.win.blit(self.MOON, (-40, 150))

        if self.main_menu:
            self._draw_menu()
        elif self.about_page:
            self._draw_about()
        elif self.controls_page:
            self._draw_controls()
        elif self.game_won:
            self._draw_won()
        elif self.game_start:
            self._update_game()
            self._draw_game()

        pygame.draw.rect(self.win, (255, 255, 255),
                         (0, 0, self.WIDTH, self.HEIGHT), 4, border_radius=10)

    def run(self) -> None:
        while self.running:
            self._handle_events()
            self._draw()
            self.clock.tick(self.FPS)
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = GameManager()
    game.run()
