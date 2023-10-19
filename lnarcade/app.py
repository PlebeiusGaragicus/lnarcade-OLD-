import os
import threading
import subprocess
import dotenv

import logging
logger = logging.getLogger()

import pygame

from lnarcade.logger import setup_logging
from lnarcade.config import MY_DIR, DOT_ENV_PATH, create_default_dot_env, FPS

APP_SCREEN: pygame.Surface = None
SCREEN_HEIGHT = None
SCREEN_WIDTH = None


class Singleton:
    _instance = None

    def __init__(self):
        # Singleton pattern must prevent normal instantiation
        raise Exception("Cannot directly instantiate a Singleton. Access via get_instance()")

    @classmethod
    def get_instance(cls):
        # This is the only way to access the one and only instance
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance



class App(Singleton):
    # window: arcade.Window = None
    screen = None
    process: subprocess.Popen = None


    @classmethod
    def get_instance(cls):
        # This is the only way to access the one and only instance
        if cls._instance:
            return cls._instance
        else:
            # Instantiate the one and only app instance
            return cls.configure_instance()


    @classmethod
    def configure_instance(cls, disable_hardware=False):

        if cls._instance:
            raise Exception("Instance already configured")

        # Instantiate the one and only app instance
        app = cls.__new__(cls)
        cls._instance = app

        print('\n\n\n\n\n###############################################')
        
        # load environment variables
        if dotenv.load_dotenv( DOT_ENV_PATH ) == False:
            # TODO: should I make this a critical error?
            print("WARNING!!!  No .env file found at {}".format(DOT_ENV_PATH))
            create_default_dot_env()
        else:
            with open(DOT_ENV_PATH, 'r') as f:
                print("DOT_ENV_PATH: %s", DOT_ENV_PATH)
                print( f.read() )

        setup_logging()
        logger.debug("Configuring application instance...")
        logger.debug("lnarcade installed at: %s", MY_DIR)

        pygame.init()
        # app.width, app.height = pygame.display.get_surface().get_size()
        app.width, app.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        logger.debug("Display size: %s x %s", app.width, app.height)

        app.screen = pygame.display.set_mode((app.width, app.height), pygame.FULLSCREEN)
        global APP_SCREEN
        APP_SCREEN = app.screen
        global SCREEN_WIDTH
        SCREEN_WIDTH = app.width
        global SCREEN_HEIGHT
        SCREEN_HEIGHT = app.height

        pygame.display.set_caption("Lightning Arcade")
        pygame.mouse.set_visible(False)

        app.clock = pygame.time.Clock()

        from lnarcade.view import ViewStateManager
        app.manager = ViewStateManager()

        from lnarcade.view.splash import SplashScreen
        app.manager.add_state("splash", SplashScreen())

        from lnarcade.view.game_select import GameSelectView
        app.manager.add_state("game_select", GameSelectView())


        ### SETUP 'HELPER' THREADS ###
        from lnarcade.control.controlmanager import ControlManager
        app.controlmanager = ControlManager()
        app.control_thread = threading.Thread(target=app.controlmanager.run)
        app.control_thread.daemon = True # this is needed so that when the main process exits the control thread will also exit

        from lnarcade.backend.server import ArcadeServerPage
        app.backend = ArcadeServerPage( DOT_ENV_PATH )
        app.backend_thread = threading.Thread(target=app.backend.start_server)
        app.backend_thread.daemon = True

        return cls._instance


    def start(self):
        logger.debug("App.get_instance().start()")

        self.control_thread.start()
        self.backend_thread.start()

        # from lnarcade.views.splash_screen import SplashScreen
        # view = SplashScreen()
        # self.window.show_view(view)
        self.manager.change_state("splash")

        try:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    self.manager.handle_event(event)

                self.manager.update()
                # self.manager.draw(self.screen)
                self.manager.draw()

                pygame.display.flip()
                self.clock.tick(FPS)

        except KeyboardInterrupt:
            logger.warning("KeyboardInterrupt")

        self.stop()

        #     pygame.quit()
        #     self.control_thread.join(0.1)
        #     self.backend_thread.join(0.1)
        #     exit(0)

        # pygame.quit()


    def kill_running_process(self):
        if self.process is None:
            logger.warning("No process to kill")
            return

        self.process.terminate()
        self.process = None


    def get_ip_addr(self):
        return subprocess.getoutput("hostname -I").split()[0]


    # def stop(self, force: bool = False):
    def stop(self):
        logger.debug("App.get_instance().stop()")
        pygame.quit()
        self.control_thread.join(0.1)
        self.backend_thread.join(0.1)
        logger.debug("App.get_instance().stop() - END")
        exit(0)
