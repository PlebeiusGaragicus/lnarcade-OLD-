TODO = """
xmen splash screen
https://www.youtube.com/watch?v=sXNzMHdLysE&list=PLDJuQJmXOz3zp3IhkvAHu4rVd3GWLSTnS
"""


import os
import time
import logging

logger = logging.getLogger()

import pygame

from lnarcade.app import APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from lnarcade.colors import *
from lnarcade.config import MY_DIR
from lnarcade.view import ViewState

# for type hinting
from pyglet.media import Player

FONT_SIZE = 30


class SplashScreen(ViewState):
    def __init__(self):
        super().__init__()
        self.alpha = 0  # initialize alpha to 0 (fully transparent)
        self.player: Player = None
        self.theme_len = 0

        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.screen = APP_SCREEN

    def setup(self):
        self.screen.fill(BLACK)
        self.start_time = time.time()

        # sound_path = os.path.join('lnarcade', 'resources', 'sounds', 'theme.wav')
        sound_path = os.path.join(MY_DIR, 'resources', 'sounds', 'theme.wav')
        self.player = pygame.mixer.Sound(sound_path)
        self.theme_len = self.player.get_length()
        self.player.play()
        

    def handle_event(self, event):
        # return super().handle_event(event)
        pass


    def update(self):
        # if os.getenv("DEBUG", False):
        #     logger.debug("DEBUG MODE: skipping splash screen")
        #     from lnarcade.app import App
        #     App.get_instance().manager.change_state("game_select")

        if time.time() > self.start_time + self.theme_len: # wait for theme to finish
            self.player.stop()

            from lnarcade.app import App
            App.get_instance().manager.change_state("game_select")


    def draw(self):
        text = self.font.render("Loading screen...", True, WHITE)
        text_with_alpha = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        text_with_alpha.fill((255, 255, 255, self.alpha))
        text_with_alpha.blit(text, (0, 0))
        self.screen.blit(text_with_alpha, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        self.alpha = min(self.alpha + 5, 255)

        # self.clear()
        # arcade.start_render()

        # color_with_alpha = arcade.color.WHITE + (self.alpha,)  # create a color object with the desired alpha value
        # arcade.draw_text("Loading screen...", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
        #                  color_with_alpha,
        #                  font_size=30, anchor_x="center")
        # self.alpha = min(self.alpha + 5, 255)  # increase alpha up to 255
