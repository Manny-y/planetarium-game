
import sys
import pygame
import threading
import time

from settings import Settings
from game_stats import Gamestats
from scoreboard import Scoreboard
from ship import Ship
from asteroid_lhs import Asteroid_lhs
from asteroid_rhs import Asteroid_rhs
from satellite import Satellite
from explosion import Explosion
from button import Button

from time import sleep
from random import randint

class Planetarium:

    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("P-P-Planetarium")

        # create an instance to store game stats
        self.stats = Gamestats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.asteroids_lhs = pygame.sprite.Group()
        self.asteroids_rhs = pygame.sprite.Group()
        self.satellite = pygame.sprite.Group()

        # Get the asteroids and satellites moving.
        threading.Thread(target=self._create_asteroids_lhs, daemon=True).start()
        threading.Thread(target=self._create_asteroids_rhs, daemon=True).start()
        threading.Thread(target=self._create_satellite, daemon=True).start()

        # Explosion
        self.explosion_group = pygame.sprite.Group()

        # Make play button
        self.play_button = Button(self, 'Play Again?')

        # Retrieve saved high score
        self.sb.retrieve_high_score()

        # Retrieve current high score
        self.sb.prep_high_score()

    def run_game(self):

        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update_movement()
                self._update_asteroids()
                self._check_asteroid_edges()

            self._update_screen()

    def _update_asteroids(self):
        # Update the positions of all asteroids in the fleet.
        self.asteroids_lhs.update()
        self.asteroids_rhs.update()
        self.satellite.update()

        if pygame.sprite.spritecollideany(self.ship, self.asteroids_lhs):
            self._planet_hit()

        if pygame.sprite.spritecollideany(self.ship, self.asteroids_rhs):
            self._planet_hit()

        if pygame.sprite.spritecollideany(self.ship, self.satellite):
            self._planet_hit()

    def _planet_hit(self):
        # Respond to the planet being hit by an asteroid or satellite.

        # Reduce the # of planets left.
        if self.stats.ships_left > 1:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
        else:
            self.stats.ships_left -= 1
            self.sb.check_high_score()
            self.sb.prep_ships()
            self.stats.game_active = False
            self.stats.reset_stats()

        # Introduce explosion
        explosion = Explosion(self.ship.rect.centerx, self.ship.rect.centery)
        self.explosion_group.add(explosion)

        # Quick pause
        time.sleep(1)

        # Get rid of any remaining asteroids and satellites.
        self.asteroids_lhs.empty()
        self.asteroids_rhs.empty()
        self.satellite.empty()

        # Center the planet again
        self.ship.recenter_planet()

        # Quick pause
        time.sleep(1)

    def _create_asteroids_lhs(self):
        # Make an asteroid from the lhs and add it to the asteroid group.
        while True:
            if len(self.asteroids_lhs) < self.settings.asteroids_allowed_lhs:
                sleep(randint(0,4))
                asteroid = Asteroid_lhs(self)
                self.asteroids_lhs.add(asteroid)

    def _create_asteroids_rhs(self):
        # Make an asteroid from the rhs and add it to the asteroid group.
        while True:
            if len(self.asteroids_rhs) < self.settings.asteroids_allowed_rhs:
                sleep(randint(0,4))
                asteroid = Asteroid_rhs(self)
                self.asteroids_rhs.add(asteroid)

    def _create_satellite(self):
        # Make a satellite.
        while True:
            if len(self.satellite) < self.settings.satellites_allowed:
                sleep(randint(0, 10))
                satellite = Satellite(self)
                self.satellite.add(satellite)

    def _check_asteroid_edges(self):
        # Remove asteroids as they go off the edge of the screen.
        for asteroid in self.asteroids_lhs.sprites():
            if asteroid.check_edges():
                self.asteroids_lhs.remove(asteroid)
                self.stats.score += self.settings.asteroid_points_lhs
                self.sb.prep_score()
                self.sb.check_high_score()

        for asteroid in self.asteroids_rhs.sprites():
            if asteroid.check_edges():
                self.asteroids_rhs.remove(asteroid)
                self.stats.score += self.settings.asteroid_points_rhs
                self.sb.prep_score()
                self.sb.check_high_score()

        for satellite in self.satellite.sprites():
            if satellite.check_edges():
                self.satellite.remove(satellite)
                self.stats.score += self.settings.satellite_points
                self.sb.prep_score()
                self.sb.check_high_score()

    def _check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.ship.rect.top > 0:
                    self.ship.moving_up = True
                elif event.key == pygame.K_DOWN and self.ship.rect.bottom < self.ship.screen_rect.bottom:
                    self.ship.moving_down = True
                elif event.key == pygame.K_LEFT and self.ship.rect.left > 0:
                    self.ship.moving_left = True
                elif event.key == pygame.K_RIGHT and self.ship.rect.right < self.ship.screen_rect.right:
                    self.ship.moving_right = True
                elif event.key == pygame.K_q:
                    sys.exit()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.ship.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.ship.moving_down = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False

    def _check_play_button(self, mouse_pos):
        # Start a new game when the player clicks play.
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.game_active = True
            self.sb.prep_score()

    def _update_screen(self):

        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        self.asteroids_lhs.draw(self.screen)
        self.asteroids_rhs.draw(self.screen)
        self.satellite.draw(self.screen)
        self.explosion_group.draw(self.screen)
        self.explosion_group.update()

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

if __name__ == '__main__':
    # Make an instance and run the game.
    pg = Planetarium()
    pg.run_game()

