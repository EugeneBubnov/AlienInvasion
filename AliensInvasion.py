import sys
import pygame
from settings import Settings
from ship import *

# Класс для управления ресурсами и поведением игры
class AlienInvasion:
    # Инициализация игры и создание ресурсов
    def __init__(self):
        pygame.init
        pygame.display.set_caption('Alien Invasion')
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.ship = Ship(self)
        self.backgroud_image = pygame.image.load('models\\background.png')
        
    def _check_events(self):
            # Чтение событий
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                sys.exit()
            elif(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_RIGHT):
                    # Переместить корабль вправо
                    self.ship.moving_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
    
    def _update_screen(self):
            #self.screen.fill(self.settings.bg_color)
            self.screen.blit(self.backgroud_image, (0, 0))
            self.ship.blitme()
            
            pygame.display.flip()
                
    def run_game(self):
        # Запуск основного цикла игры
        while(True):
            self._check_events()
            self.ship.update()
            self._update_screen()
                        
if __name__ == '__main__':
    #Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()