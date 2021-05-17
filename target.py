import pygame
import random
from pygame.sprite import Sprite


class Target(Sprite):
    # A class to represent a single target.
    def __init__(self, tpgame):
        # Initialize the target and set its starting position.
        super().__init__()
        self.screen = tpgame.screen
        self.settings = tpgame.settings

        # Load the target image and set its rect attribute.
        self.image = pygame.image.load('images/Target.png')
        self.rect = self.image.get_rect()

        # Start each new target at a random place in the screen.
        self.rect.x = random.randrange(0, int(self.screen.get_rect().width))
        self.rect.y = random.randrange(0, int(self.screen.get_rect().height))

        # Store the target's exact position.
        self.pos = self.rect
        self.pos.x = float(self.rect.x)
        self.pos.y = float(self.rect.y)

    def blitme(self):
        # Draw the target at its current location.
        self.screen.blit(self.image, self.rect)
