import os
import platform
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
    def configure_instance(cls):

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

        ret = pygame.init()
        logger.debug("pygame.init() returned: %s", ret)

        # pygame.font.init()
        # app.width, app.height = pygame.display.get_surface().get_size()
        # app.width, app.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        _vid_info = pygame.display.Info()
        app.width, app.height = _vid_info.current_w, _vid_info.current_h

        logger.debug("Display size: %s x %s", app.width, app.height)

        # NOTE: DON'T DO FULLSCREEN FOR THE LOVE OF GOD!!!
        app.screen = pygame.display.set_mode((app.width, app.height), flags=pygame.NOFRAME)
        # app.screen = pygame.display.set_mode((app.width, app.height), pygame.FULLSCREEN)
        # app.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)

        global APP_SCREEN
        APP_SCREEN = app.screen
        global SCREEN_WIDTH
        SCREEN_WIDTH = app.screen.get_width()
        global SCREEN_HEIGHT
        SCREEN_HEIGHT = app.screen.get_height()

        pygame.display.set_caption("Lightning Arcade")
        pygame.mouse.set_visible(False)

        app.process = None

        app.clock = pygame.time.Clock()

        from lnarcade.view import ViewStateManager
        app.manager = ViewStateManager()

        from lnarcade.view.splash import SplashScreen
        app.manager.add_state("splash", SplashScreen())

        from lnarcade.view.game_select import GameSelectView
        app.manager.add_state("game_select", GameSelectView())


        ### SETUP 'HELPER' THREADS ###
        # if platform.system() != 'Darwin':
        #     from lnarcade.control.controlmanager import ControlManager
        #     app.controlmanager = ControlManager()
        #     app.control_thread = threading.Thread(target=app.controlmanager.run)
        #     app.control_thread.daemon = True # this is needed so that when the main process exits the control thread will also exit
        # else:
        #     app.controlmanager = None
        app.controlmanager = None

        # from lnarcade.backend.server import ArcadeServerPage
        # app.backend = ArcadeServerPage( DOT_ENV_PATH )
        # app.backend_thread = threading.Thread(target=app.backend.start_server)
        # app.backend_thread.daemon = True
        app.backend_thread = None

        return cls._instance


    def start(self):
        logger.debug("App.get_instance().start()")


        if self.controlmanager is not None:
            logger.debug("starting the control thread")
            self.control_thread.start()
        else:
            logger.debug("skipping the control thread (becuase we're on MacOS))")

        if self.backend_thread is not None:
            logger.debug("starting the backend thread")
            self.backend_thread.start()
        else:
            logger.debug("skipping the backend thread)")


        self.manager.change_state("splash")
        # self.manager.change_state("game_select")

        try:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False
                    self.manager.handle_event(event)

                self.manager.update()
                # self.manager.draw(self.screen)
                self.manager.draw()

                pygame.display.flip()
                self.clock.tick(FPS)

        except KeyboardInterrupt:
            logger.warning("KeyboardInterrupt")
        
        # except NotImplementedError:
        #     logger.critical("NotImplementedError")

        #     from lnarcade.view.error import ErrorModalView
        #     self.manager.add_state("error", ErrorModalView("NotImplementedError", None))
        #     self.manager.change_state("error")

            # while True:
            #     for event in pygame.event.get():
            #         if event.type == pygame.QUIT:
            #             running = False
            #         self.manager.handle_event(event)

            #     self.manager.draw()

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
        logger.debug("App.get_instance().stop(): quitting pygame and joining threads...")
        pygame.quit()
        if self.controlmanager is not None:
            self.control_thread.join(0.1)
            # self.controlmanager.stop() # TODO stop or join:

        if self.backend_thread is not None:
            self.backend_thread.join(0.1)
            # self.backend.stop() # TODO stop or join:

        logger.debug("App.get_instance().stop() - DONE - END")
        exit(0)
