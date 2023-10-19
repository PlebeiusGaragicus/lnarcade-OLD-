import os
import time
import logging
logger = logging.getLogger()

from dataclasses import dataclass
import subprocess


import pygame

from lnarcade.app import App, APP_SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from lnarcade.config import APP_FOLDER, MY_DIR
from lnarcade.colors import *
from lnarcade.utilities.find_games import get_app_manifests
from lnarcade.view import ViewState
# from lnarcade.view.error import ErrorModalView



@dataclass
class GameListItem:
    module_name: str
    game_name: str
    manifest_dict: dict
    image_path: str
    image: pygame.Surface = None

    def __post_init__(self):  # This method is automatically called after `__init__`
        try:
            self.image = pygame.image.load(self.image_path)
        except pygame.error:  # Pygame raises a generic error for file not found
            image_path = os.path.expanduser(f"{MY_DIR}/resources/img/missing.jpg")
            self.image = pygame.image.load(image_path)




class GameSelectView(ViewState):
    def __init__(self):
        super().__init__()
        self.screen = APP_SCREEN
        self.alpha = 0  # initialize alpha to 0 (fully transparent)
        self.mouse_pos = (0, 0)
        self.selected_index = 0
        self.last_input_time = time.time()
        self.menu_items: list = []
        self.credits: int = 0

        self.A_held = False
        self.show_mouse_pos = False

        manifests = get_app_manifests()
        logger.debug("manifests: %s", manifests)

        for (app_folder_name, manifest_dict) in manifests.items():
            image_path = os.path.expanduser(f"~/{APP_FOLDER}/{app_folder_name}/image.png")

            try:
                game_name = f"{manifest_dict['name']}"

                self.menu_items.append( GameListItem(app_folder_name, game_name, manifest_dict, image_path) )
            except KeyError:
                logger.error(f"KeyError in {app_folder_name} manifest.json")
                continue

        logger.debug("self.menu_items: %s", self.menu_items)


    def setup(self):
        # arcade.set_background_color(arcade.color.BLACK)
        self.screen.fill(BLACK)

        # TODO - clean this up...
        if self.menu_items == []:
            App.get_instance().window.show_view( ErrorModalView("No manifests found!", None) )


    def update(self):
        pass
        # simulate keypress
        # if time.time() - self.last_input_time > int(os.getenv("AFK_SCROLL_TIME", 300)):
            # self.on_key_press(arcade.key.DOWN, 0)


    def draw(self):
        # SHOW GAME ARTWORK
        image = self.menu_items[self.selected_index].image
        scaled_image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scaled_image, (0, 0))  # Drawing the image

        # Define the coordinates for the gradient effect.
        left = 0
        right = int(SCREEN_WIDTH * 0.5)
        top = SCREEN_HEIGHT
        bottom = 0

        # Gradient Effect
        gradient_strength = 1
        gradient_rect_width = 5
        for i in range(0, SCREEN_WIDTH // 2, gradient_rect_width):
            alpha = int(255 * gradient_strength * ((SCREEN_WIDTH // 2 - i) / (SCREEN_WIDTH // 2)))
            gradient_surface = pygame.Surface((gradient_rect_width, SCREEN_HEIGHT), pygame.SRCALPHA)
            gradient_surface.fill((0, 0, 0, alpha))
            self.screen.blit(gradient_surface, (i, 0))


        # Drawing Texts
        font_30 = pygame.font.SysFont(None, 30)
        font_45 = pygame.font.SysFont(None, 45)
        x, y = SCREEN_WIDTH * 0.02, SCREEN_HEIGHT // 2
        offset = y + self.selected_index * 55


        for i, menu_item in enumerate(self.menu_items):
            color = (173, 173, 239)  # arcade.color.BLUE_BELL
            menu_item_size = 30
            if i == self.selected_index:
                color = (255, 255, 255)  # arcade.color.WHITE
                menu_item_size = 45
                text = font_45.render(menu_item.game_name, True, color)
            else:
                text = font_30.render(menu_item.game_name, True, color)

            self.screen.blit(text, (x, offset - i * 55))

        # Drawing game type
        try:
            game_type = self.menu_items[self.selected_index].manifest_dict["type"]
            text = font_30.render(game_type, True, (255, 0, 0))  # arcade.color.RED
            self.screen.blit(text, (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.05))
        except KeyError:
            pass



        # self.flash_free_play()
        # self.show_configuration()

        # SHOW MOUSE POSITION
        # if os.getenv("DEBUG", False):
            # self.show_mouse_position()


    def on_key_press(self, symbol: int, modifiers: int):
        self.last_input_time = time.time()

        if symbol == arcade.key.UP:
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
        elif symbol == arcade.key.DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)
        
        elif symbol == arcade.key.A:
            self.A_held = True
        elif symbol == arcade.key.B:
            self.show_mouse_pos = not self.show_mouse_pos

        # QUIT
        elif symbol == arcade.key.ESCAPE:
            arcade.Window.close( GAME_WINDOW )
            exit(0)

        # elif symbol == arcade.key.TAB:
        #     if self.process is not None:
        #         # self.process.kill()
        #         self.process.terminate()
        #         self.process = None

        # LAUNCH APP
        elif symbol == arcade.key.ENTER:
            selected_app = self.menu_items[self.selected_index].module_name
            logger.debug("Launching python module: %s", selected_app)


            # check for sufficient 'coins'
            logger.debug("Checking for sufficient coins")
            if not os.getenv("FREE_PLAY", False):
                # toast("Excuse me... YOU NEED TO PAY UP!!") #TODO
                logger.error("You don't have enough coins")
                return


            # doesn't do anything...?  Is it because I'm no in a draw loop or something????
            # arcade.set_background_color(arcade.color.BLACK)
            # arcade.start_render()
            
            # DEPRECATED:
            # if FULLSCREEN:
                # self.window.set_fullscreen(False)
            # self.window.set_visible(False) # doesn't do anything...?
            # self.window.minimize()

            args = ["python3", "-m", selected_app]
            cwd = os.path.expanduser(f"~/{APP_FOLDER}")
            logger.debug(f"subprocess.run({args=}, {cwd=})")
            # ret_code = subprocess.run(args, cwd=cwd).returncode # This is a blocking call - wait for game to run and exit

            # self.process = subprocess.Popen(args, cwd=cwd)
            App.get_instance().process = subprocess.Popen(args, cwd=cwd)

            # if ret_code != 0:
            #     logger.error(f"app '{selected_app}' returned non-zero! {ret_code=}")
            #     self.window.show_view( ErrorModalView("App crashed!", self) )

            # arcade.set_background_color(arcade.color.BLACK)
            # self.window.set_visible(True) # doesn't do anything...?
            # self.window.maximize()

            # DEPRECATED:
            # if FULLSCREEN:
            #     self.window.set_fullscreen(True)

    def on_key_release(self, key: int, modifiers: int):
        if key == arcade.key.A:
            self.A_held = False


    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_pos = (x, y)
        # return super().on_mouse_motion(x, y, dx, dy)
    

    def show_mouse_position(self):
        if self.show_mouse_pos is False:
            return

        anchor_x = "left"
        offset = 20

        if self.mouse_pos[0] > SCREEN_WIDTH * 0.5:
            anchor_x = "right"

        if self.mouse_pos[1] > SCREEN_HEIGHT * 0.5:
            offset -= offset * 2

        arcade.draw_text(f"{self.mouse_pos}", self.mouse_pos[0], self.mouse_pos[1] + offset, arcade.color.WHITE, font_size=16, anchor_x=anchor_x)
        arcade.draw_text(f"{round(self.mouse_pos[0] / SCREEN_WIDTH * 100, 0)}%  {round(self.mouse_pos[1] / SCREEN_HEIGHT * 100, 0)}%", self.mouse_pos[0], self.mouse_pos[1] + offset * 2, arcade.color.GREEN, font_size=16, anchor_x=anchor_x)
        arcade.draw_point(self.mouse_pos[0], self.mouse_pos[1], arcade.color.RED, 5)


    def flash_free_play(self):
        if os.getenv("FREE_PLAY", False):
            # alpha = abs((time.time() % 4) - 1)  # calculate alpha value for fade in/out effect
            alpha = abs((time.time() % 2) - 1)  # calculate alpha value for fade in/out effect
            arcade.draw_text("FREE PLAY", 10, 10, arcade.color.GREEN + (int(alpha * 255),), font_size=26, anchor_x="left")
        else:
            alpha = abs((time.time() % 2) - 1)  # calculate alpha value for fade in/out effect
            arcade.draw_text(f"CREDITS: {self.credits}", 10, 10, arcade.color.RED + (int(alpha * 255),), font_size=26, anchor_x="left")


    def show_configuration(self):
        if self.A_held is False:
            return

        ip = App.get_instance().get_ip_addr()
        arcade.draw_text(f"IP: {ip}:8080", SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.05, arcade.color.GRAPE, font_size=16, anchor_x="center")
