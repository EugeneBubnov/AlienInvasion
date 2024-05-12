import sys
import pygame
from settings import settings
from ship import *
from bullet import *
from alien import Alien

# Класс для управления ресурсами и поведением игры
class AlienInvasion:
    # Инициализация игры и создание ресурсов
    def __init__(self):
        pygame.init()  # game init
        pygame.display.set_caption('Alien Invasion')  # Title
        self.settings = settings()  # init class settings()
        self.backgroud_image = pygame.image.load('models\\background.png')
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)  # Display size

        self.ship = Ship(self)  # init spaceship
        self.bullets = pygame.sprite.Group()  # Container for sprites group
        self.aliens = pygame.sprite.Group()  # Container for sprites group
        self._create_fleet()

    def _create_fleet(self):
        alien = Alien(self)
        self.aliens.add(alien)

    # Bullets
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

    # Events checker(keyboard actions)
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # move to right
            self.ship.moving_right = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # move to left
                self.ship.moving_left = True
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.ship.moving_left = False

    def _check_events(self):
        # Чтение событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_screen(self):
        self.screen.blit(self.backgroud_image, (0, 0))
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        pygame.display.flip()

    # Main game cycle.
    def run_game(self):
        # Запуск основного цикла игры
        while (True):
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()