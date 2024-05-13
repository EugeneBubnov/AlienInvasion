import sys
import pygame
from settings import settings
from ship import *
from bullet import *
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

# Класс для управления ресурсами и поведением игры
class AlienInvasion:
    # Инициализация игры и создание ресурсов
    def __init__(self):
        pygame.init()  # game init
        pygame.display.set_caption('Alien Invasion')  # Title
        self.settings = settings()  # init class settings()
        self.backgroud_image = pygame.image.load('models\\background.png')
        self.screen = pygame.display.set_mode(
            (1366, 768), pygame.FULLSCREEN)  # Display size
        self.stats = GameStats(self)
        self.ship = Ship(self)  # init spaceship
        self.sb = Scoreboard(self)
        self.bullets = pygame.sprite.Group()  # Container for sprites group
        self.aliens = pygame.sprite.Group()  # Container for sprites group
        self._create_fleet()
        self.play_button = Button(self, "Play")
    
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break
        
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            
            self.aliens.empty()
            self.bullets.empty()
            
            self._create_fleet()
            self.ship.center_ship()
            sleep(0,5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)
        
    def _update_aliens(self):
        #self._check_fleet_edges()
        self.aliens.update()
        
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print('Ship hit!')
            self._ship_hit()
        self._check_aliens_bottom()
        
    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width # - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
        
    def _check_bullet_aliens_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

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
        # print(len(self.bullets))
        self._check_bullet_aliens_collisions()   
        
    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = True
            pygame.mouse.set_visible(False) 
            self.sb.prep_score()    

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_screen(self):
        self.screen.blit(self.backgroud_image, (0, 0))
        self.ship.blitme()
        if not self.stats.game_active:
            self.play_button.draw_button()  
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.sb.show_score()    
        self.aliens.draw(self.screen)
      
        
        pygame.display.flip()
    
    # Main game cycle.
    def run_game(self):
        # Запуск основного цикла игры
        while (True):
            self._check_events()
            
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._check_fleet_edges()
                self._update_aliens()
            self._update_screen()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
