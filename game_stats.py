import shelve

class Gamestats:
    # Track any statistics for the game.

    def __init__(self, pg_game):
        # Initialise statistics.
        self.settings = pg_game.settings
        self.reset_stats()
        self.screen = pg_game.screen

        # Game playing status.
        self.game_active = True

        # Highest score for the game.
        self.high_score = 0

    def reset_stats(self):
        # Initialise statistics that can change during the game.
        self.ships_left = self.settings.planet_limit
        self.score = 0




