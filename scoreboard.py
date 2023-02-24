import pygame.font
import pickle

from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    # A class to report scoring information

    def __init__(self, pg_game):
        # Initialise score keeping attributes.
        self.pg_game = pg_game
        self.screen = pg_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = pg_game.settings
        self.stats = pg_game.stats
        self.prep_ships()

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 35)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        # Turn the score into a rendered image.
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 10

    def prep_high_score(self):
        high_score = round(self.stats.high_score)
        high_score_str = '{:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_ships(self):
        # show how many ships are left.
        self.planets = Group()
        for ship_number in range(self.stats.ships_left):
            planet = Ship(self.pg_game)
            planet.rect.x = 10 + ship_number * (planet.rect.width * 0.5)
            planet.rect.y = 5
            self.planets.add(planet)

    def show_score(self):
        # Draw planet lives remaining on the screen.
        self.planets.draw(self.screen)

        # Draw accumulated points on the screen.
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def check_high_score(self):
        # Check to see if there's a new high score.
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

            # Save the new high score down in the .txt file.
            with open('high_score.txt', 'wb') as file:
                pickle.dump(self.stats.high_score, file)

    def retrieve_high_score(self):
        # Get the highest score stored on file.
            try:
                with open('high_score.txt', 'rb') as file:
                    self.stats.high_score = pickle.load(file)
            except:
                print(pickle.load(file))

