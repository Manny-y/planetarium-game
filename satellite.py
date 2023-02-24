import pygame
from random import randint
from pygame.sprite import Sprite

class Satellite(Sprite):

    def __init__(self, pg_game):
        super().__init__()
        self.screen = pg_game.screen
        self.settings = pg_game.settings

        # Loan asteroid image and set its rect attribute.
        self.image = pygame.image.load('images/satellite.bmp')
        self.image = pygame.transform.scale(self.image, (25, 25))
        self.rect = self.image.get_rect()

        # Start each asteroid near the top left of the screen.
        self.rect.y = randint(0, self.settings.screen_width)
        self.rect.x = -self.rect.height

        # Store the asteroid's exact position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        # Return True if asteroid has gone past the edge of screen.
        screen_rect = self.screen.get_rect
        if self.rect.right >= (self.settings.screen_width + self.rect.width)\
                or self.rect.left <= (0 - self.rect.width):
            return True

    def update(self):
        # Move the asteroid to the right
        self.x += self.settings.satellite_speed * self.settings.satellite_direction
        self.y += self.settings.satellite_speed * self.settings.rand_satellite_direction
        self.rect.x = self.x
        self.rect.y = self.y





