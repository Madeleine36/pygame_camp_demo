# # taken (and edited) from
# https://realpython.com/pygame-a-primer/

# Import the pygame module
import pygame as pg
from pygame.math import Vector2


# Import random for random numbers
from math import inf, pi
import time
import sys
import logging


log_file = "test_rpg.log"
logging.basicConfig(level=logging.INFO, filemode="a")

f = logging.Formatter(
    "Logger: %(name)s: %(levelname)s at: %(asctime)s, line %(lineno)d: %(message)s"
)
stdout = logging.StreamHandler(sys.stdout)
rpg_log = logging.FileHandler(log_file)
stdout.setFormatter(f)
rpg_log.setFormatter(f)

logger = logging.getLogger("Test RPG")
logger.addHandler(rpg_log)
logger.addHandler(stdout)
logger.info("Program started at {}".format(time.time()))

# Import pygame.locals for easier access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    QUIT,
    K_d,
    K_s,
    K_w,
    K_SPACE,
    K_RETURN,
    USEREVENT
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


# Define the Player object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(pg.sprite.Sprite):
    def __init__(self,parent):
        super(Player, self).__init__()
        
        self.surf = pg.image.load("dragon.png").convert_alpha()
        self.surf = pg.transform.scale(self.surf,(50,50))
        self.parent = parent

        self.original_surf = self.surf
        self.rect = self.surf.get_rect()
        logger.info('initial player width height {} {}'.format(self.rect.width,self.rect.height))
        self.hor_speed = 0
        self.vert_speed = 0

        self.hor_accel = 8
        self.vert_accel = 8

class MyGame:
    def __init__(self):
        # Initialize pygame

        pg.init()

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.WINDOW_RES = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pg.display.set_mode(self.WINDOW_RES)
        pg.display.set_caption('Pygame Test')

        self.fill_color = (255,255,255)
        self.screen.fill(self.fill_color)
        background_img = pg.image.load('sky.jpg')
        background_surf = pg.Surface.convert_alpha(background_img)
        self.BACKGROUND = pg.transform.scale(background_surf, self.WINDOW_RES)
        self.screen.blit(self.BACKGROUND,(0,0))
        
        self.fps = 30


        # Create our 'player'
        self.player = Player(self)
        # player position is its centre
        self.player.pos = Vector2(30,30)
        self.player.rect = self.player.surf.get_rect(center=self.player.pos)
        self.player.radius = 25 

        

        # Create groups to hold enemy sprites, and every sprite
        # - all_sprites is used for rendering
        self.all_sprites = pg.sprite.Group()

        # adding player to spritegroup after walls so it will display on top
        self.all_sprites.add(self.player)

        # Setup the clock for a decent framerate
        self.clock = pg.time.Clock()

    def update(self):
        '''
        moves player and other stuff
        draws objects on screen
        '''

        self.update_player()


        # Fill the screen
        self.screen.fill(self.fill_color)
        self.screen.blit(self.BACKGROUND,(0,0))

        # Draw all our sprites
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        # Flip everything to the display
        pg.display.flip()

        # Ensure program maintains a rate of 30 frames per second
        self.clock.tick(self.fps)

    def update_player(self):

        # horizontal speed
        self.player.pos[0] += self.player.hor_speed
        # and vertical speed
        self.player.pos[1] += self.player.vert_speed


        # update rect for display purposes
        self.player.rect.center = (self.player.pos[0], self.player.pos[1])


    def run(self):
         # Variable to keep our main loop running
        self.running = True

        # Our main loop
        while self.running:
            # Look at every event in the queue
            for event in pg.event.get():
                # Did the user hit a key?
                if event.type == QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_LEFT:
                        # self.player.rot_speed = -self.player.rot_accel
                        self.player.hor_speed = -self.player.hor_accel
                    elif event.key == K_RIGHT:
                        # self.player.rot_speed = self.player.rot_accel
                        self.player.hor_speed = self.player.hor_accel
                    elif event.key == K_UP:
                        self.player.vert_speed = -self.player.vert_accel
                    elif event.key == K_DOWN:
                        self.player.vert_speed = self.player.vert_accel    
                elif event.type == KEYUP:
                    if event.key == K_LEFT or event.key == K_RIGHT:
                        self.player.hor_speed = 0
                    elif event.key == K_UP or event.key == K_DOWN:
                        self.player.vert_speed = 0

            self.update()


            

if __name__ == '__main__':
    game = MyGame()
    game.run()

