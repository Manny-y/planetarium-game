import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, pg_game):
        super().__init__()

        self.screen = pg_game.screen
        self.settings = pg_game.settings

        self.ship = pygame.image.load('images/earth.bmp')
        self.image = pygame.image.load('images/heart.bmp')
        self.rect = self.ship.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.rect.center = self.screen_rect.center
        # self.rect.bottom = self.screen_rect.center

        # Movement flag
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False


    def update_movement(self):
        """Update the planets position based on the movement flag."""
        if self.moving_left and self.rect.left > self.settings.planet_speed:
            self.rect.centerx -= self.settings.planet_speed
        if self.moving_right and self.rect.right < (self.screen_rect.right - self.settings.planet_speed):
            self.rect.centerx += self.settings.planet_speed
        if self.moving_up and self.rect.top > self.settings.planet_speed:
            self.rect.bottom -= self.settings.planet_speed
        if self.moving_down and self.rect.bottom < (self.screen_rect.bottom - self.settings.planet_speed):
            self.rect.bottom += self.settings.planet_speed

    def recenter_planet(self):
        """Recenter the ship on the screen."""
        self.rect.center = self.screen_rect.center
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.ship, self.rect)
