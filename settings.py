from random import randint

class Settings():

    def __init__(self):
        # Screen settings
        self.screen_width = 450
        self.screen_height = 450
        self.bg_color = (204, 233, 255, 255)
        self.asteroids_allowed_lhs = randint(2,8)
        self.asteroids_allowed_rhs = randint(2,8)
        self.satellites_allowed = 2

        # Asteroid settings
        self.asteroid_speed = 1
        # Asteroid direction of 1 represents right; -1 represents left.
        self.asteroid_direction = 1
        self.rand_asteroid_direction = 0

        # Satellite settings
        self.satellite_speed = 1
        self.satellite_direction = 1
        self.rand_satellite_direction = 0

        # Ship settings
        self.planet_speed = 2
        self.planet_limit = 3

        # Scoring points
        self.asteroid_points_lhs = 10
        self.asteroid_points_rhs = 8
        self.satellite_points = 5
