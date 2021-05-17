class Settings:
    # A class to store all of the settings for Alien Invasion.

    def __init__(self):
        # Initialize the game's settings.
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 1

        # How quickly the game speeds up.
        self.speedup_scale = 1.1
        self.targetLife_scale = 0.8

        # How quickly the targets' worth increases.
        self.worth_scale = 1.5

        #The maximum framerate that the game runs at.
        self.framerate = 60

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 10
        self.bullet_speed = 15

        # Target settings.
        self.targetLife = 60
        self.targetWorth = 50

        # Fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.targetLife *= self.targetLife_scale
        self.targetWorth = int(self.targetWorth * self.worth_scale)
        print(self.targetWorth)
