class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, tp_game):
        """Initialize statistics"""
        self.settings = tp_game.settings
        self.reset_stats()
        self.game_active = False
        # High Score shouldn't be reset.
        with open("highscore.txt", "r+") as self.score_file:
            self.high_score = int(self.score_file.read())
            self.score_file.close()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
