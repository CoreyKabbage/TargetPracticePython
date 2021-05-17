import sys, random, time

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from target import Target
from game_stats import GameStats
from button import Button
from interface import Lives
from interface import ScoreBoard

class TargetPractice:
    # Overall class to manage game assets and behavior.

    def __init__(self):
        # Initialize the game and create game resources
        pygame.init()
        self.settings = Settings()
        self.sysfont = pygame.font.get_default_font()

        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1280, 720))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Target Practice")

        self.bg_color = self.settings.bg_color
        self.framerate = self.settings.framerate

        # Create an instance to store game statistics.
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)

        # Make the play button.
        self.play_button = Button(self, "Play")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.targets = pygame.sprite.Group()

        self.timer = pygame.time.Clock()

        #starter tick
        self.start_ticks = pygame.time.get_ticks()

        # seconds for the target lifetime timer.
        self.seconds = 0
        self.targets_hit = 0

        # font for the target lifetime timer.
        self.timerfont = pygame.font.Font("Pixellettersfull.ttf", 32)

        self.timertext = self.timerfont.render("0", True, (0, 0, 0),
self.settings.bg_color)

        self.timerrect = self.timertext.get_rect()

        #Lives display
        self.lives = pygame.sprite.Group()
        self.lives_left = self.settings.ship_limit

        #Texts for game over screen and time out.
        self.infofont = pygame.font.Font("Pixellettersfull.ttf", 48)
        self.game_over_text = self.infofont.render("Game Over", 1, (255, 100, 100))
        self.time_out_text = self.infofont.render("Time up!", 1, (255, 100, 100))

        self.game_over_rect = self.game_over_text.get_rect()
        self.time_out_rect = self.time_out_text.get_rect()

        self.game_over_wait = 200
        self.time_out_wait = 200

        self.game_over_flag = False

    def _check_events(self):
        # Watch for keyboard and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        # Respond to key presses.
            if event.key == pygame.K_RIGHT:
                # Move the ship to the right.
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                # Move the ship to the left.
                self.ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
            elif event.key == pygame.K_ESCAPE:
                self.stats.score_file = open("highscore.txt", "w")
                self.stats.score_file.write(self.stats.high_score)
                self.stats.score_file.close()
                sys.exit()

    def _check_keyup_events(self, event):
        # Respond to key releases.
        if event.key == pygame.K_RIGHT:
            # Stop movement when key released.
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # Stop movement when key released.
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True

            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Get rid of any remaining aliens and bullets.
            self.targets.empty()
            self.bullets.empty()

            # Create a new fleet, and center the ship.
            self._create_target()
            self.ship.center_ship()

            # Prep score and level.
            self.sb.prep_score()
            self.sb.prep_level()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        # Create a bullet and add it to the bullets group.
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _ship_hit(self):
        """respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1

            #Time Out Text
            self.time_out_rect.center = self.screen.get_rect().center
            self.screen.blit(self.time_out_text, self.time_out_rect)

            pygame.display.update()
            time.sleep(1)

            # Get rid of any remaining aliens and bullets.
            self.targets.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_target()
            self.ship.center_ship()

            #Decrement the lives display.
            lives = self.lives.sprites()
            lost_life = lives[-1]
            self.lives.remove(lost_life)
            self._draw_lives()


            # Pause.
            time.sleep(0.5)
        else:
            self.game_over_flag = True
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_target(self):
        # Create a target and place it randomly.
        self.target = Target(self)
        target_width, target_height = self.target.rect.size
        self.target.x = random.randrange(int(self.screen.get_rect().width))
        self.target.rect.x = self.target.x
        self.target.y = random.randrange(int(self.screen.get_rect().height *
0.75))
        self.target.rect.y = self.target.y
        self.targets.add(self.target)

    def _update_targets(self):
        """Update the positions of all targets in the fleet."""
        self.targets.update()
        # Look for target-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.targets):
            self._ship_hit()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets"""
        # Update bullet positions.
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_target_collisions()

    def _check_bullet_target_collisions(self):
        # Check for any bullets that have hit targets.
        #  If so, get rid of the bullet and the target.
        collisions = pygame.sprite.groupcollide(self.bullets, self.targets,
True, True)

        if collisions:
            for targets in collisions.values():
                self.targets_hit +=1
                self.stats.score += self.settings.targetWorth * len(targets)
                self.sb.prep_score()
                self.sb.check_high_score()


        if not self.target in self.targets:
            self._start_new_level()

    def _start_new_level(self):
        # Destroy existing bullets and create new fleet.
        self.bullets.empty()
        self._create_target()
        self.targets_hit += 1
        self._reset_timer()
        if self.targets_hit > 10:
            self.targets_hit = 0
            self.stats.level += 1
            self.sb.prep_level()
            self.settings.increase_speed()

    def _update_timer(self):
        self.timer.tick(self.framerate)

    def _check_time(self):
        self.seconds += self.timer.get_time() / 1000
        self.timertext = self.timerfont.render(str(int(self.seconds)), True,
(0, 0,
0),
(255, 255, 255))
        self.timerrect = self.timertext.get_rect()
        self.timerrect.midtop = self.screen.get_rect().midtop


    def _reset_timer(self):
        self.seconds = 0

    def _init_lives(self):
        lives_left = self.lives_left
        for life_number in range(lives_left):
            life = Lives(self)
            life_width, life_height = life.rect.size
            life.x = life_width + 2 * life_width * life_number
            life.rect.x = life.x
            self.lives.add(life)

    def _draw_lives(self):
        self.lives.draw(self.screen)

    def _update_screen(self):
            # Update images on screen and flip to the new screen.
            self.screen.fill(self.bg_color)
            self.ship.blitme()
            self._draw_lives()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.targets.draw(self.screen)
            self.sb.show_score()
            self.screen.blit(self.timertext, self.timerrect)

            # Draw the play button if the game is inactive.
            if not self.stats.game_active and self.game_over_flag == False:
                self.play_button.draw_button()
            elif not self.stats.game_active and self.game_over_flag == True:
                self.game_over_rect.center = self.screen.get_rect().center
                self.game_over_rect.y = self.game_over_rect.y - 50
                self.screen.blit(self.game_over_text, self.game_over_rect)
                self.play_button.draw_button()
                pygame.display.update()
                self.settings.initialize_dynamic_settings()

            # Make the most recently drawn screen visible.
            pygame.display.flip()

    def run_game(self):
        self._init_lives()
        # Start the main loop for the game.
        while True:
            self._check_events()

            if self.stats.game_active:
                self._update_timer()
                self._check_time()
                self.ship.update()
                self._update_bullets()
            '''When 3 seconds passes without the target being hit, restart the
            game and remove a life.'''
            if self.seconds > 4:
                self.targets.empty()
                self._reset_timer()
                self._create_target()
                self._ship_hit()


            self._update_screen()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    tp_game = TargetPractice()
    tp_game.run_game()
