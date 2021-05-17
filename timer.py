import sys, os
import pygame

class TargetTimer():
    def __init__(self, tpgame):
        self.framerate = tpgame.settings.framerate
        self.timeup = False
    
    def _update_timer(self, tpgame):
        targetLife = int(tpgame.settings.targetLife)
        timeup = self.timeup
        pygame.time.set_timer(timeup, targetLife, True)
    
    def _reset_timer(self):
        timeup = self.timeup
        pygame.time.set_timer(timeup, 0)
