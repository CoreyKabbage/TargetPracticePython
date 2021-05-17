class GameStats:
    """Track statistics for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        # High Score shouldn't be reset.
        self.score_file = open("highscore.txt", "r")
        if not self.score_file:
            self.score_file.write(0)
        self.high_score = int(self.score_file.read())

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
