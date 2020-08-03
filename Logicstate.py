import sys, os
import pygame
from pygame.locals import *
import numpy as np
import math
from PIL import Image

size = width, height = 448, 256
black = 0, 0, 0
white = 255, 255, 255

background = 0, 140, 178


TILESIZE = 60
TILESIZE_X = TILESIZE
TILESIZE_Y = TILESIZE

TILEMAP_W = width // TILESIZE_X + 1

TILEMAP_H = height // TILESIZE_Y + 1

MAP_TOTAL = (TILEMAP_W)*(TILEMAP_H)

texture_file = 'data/resize60/'

texture_ID = ['water', 'sand', 'grass']

textures = {texture_ID[0]:[texture_file + f"water-files/water-plain-{i}.png" for i in range(60)],
            texture_ID[1]:[texture_file + f"sand-files/sand-texture-{i}.png" for i in range(49)],
            texture_ID[2]:[texture_file + f"grass-files/grass-texture-{i}.png" for i in range(6)]}

playermode = ['down', 'right', 'up', 'left']

player_anim_sprite = {playermode[0]: [f"data/sprites/sprite-{i}-small.png" for i in [6, 7, 8]],
                    playermode[1]: [f"data/sprites/sprite-{i}-small.png" for i in [3, 4, 5]],
                    playermode[2]: [f"data/sprites/sprite-{i}-small.png" for i in [0, 1, 2]],
                    playermode[3]: [f"data/sprites/sprite-{i}-small.png" for i in [9, 10, 11]],
                    }



class Camera():
    def __init__(self):
        pass
        
    def DrawRender(self, screen, Player, Tilemap = [[1, 0, 1, 0, 1],[0, 1, 0, 1, 0],[1, 0, 1, 0, 1],[0, 1, 0, 1, 0],[1, 0, 1, 0, 1]]):
        if Tilemap.shape[0] > TILEMAP_W or Tilemap.shape[1] > TILEMAP_H:
            Tilemap = Tilemap[:TILEMAP_W, :TILEMAP_H]
        screen_offset_x = 0
        screen_offset_y = 0
        for Left_start_col in Tilemap:
            for topmost_ID in Left_start_col:
                new_surface = pygame.image.load(textures[texture_ID[topmost_ID]][3])
                screen.blit(new_surface, [screen_offset_x, screen_offset_y])
                screen_offset_y += TILESIZE
                
            screen_offset_x += TILESIZE
            screen_offset_y = 0

            #vertical scan lines!
                

        if Player.viewable:
            new_surface = pygame.image.load(Player.sprite)
            new_surface = new_surface.convert()
            colorkey = new_surface.get_at((0,0))
            new_surface.set_colorkey(colorkey, RLEACCEL)
            
            screen.blit(new_surface, [Player.X, Player.Y])
        
                
            
class Player():
    def __init__(self, world_coordinate = [width // 2, height // 2]):
        self.X = world_coordinate[0]
        self.Y = world_coordinate[1]
        self.velocity_x = 0
        self.velocity_y = 0
        self.viewable = True
        self.mode = 'down'
        self.walking = False
        self.sprite = player_anim_sprite[self.mode][1]
        self.walking_count = 2
                

    def step_animation(self):
        
        self.walking_count -= 1
        if self.walking_count < 0:
            self.walking_count = 2

        self.sprite = player_anim_sprite[self.mode][self.walking_count]

    def accelerate(self):
        if self.mode == 'down':
            self.velocity_y = 1
        elif self.mode == 'left':
            self.velocity_x = -1
        elif self.mode == 'up':
            self.velocity_y = -1
        elif self.mode == 'right':
            self.velocity_x = 1

    def update_position(self):
        self.X += self.velocity_x
        self.Y += self.velocity_y
        
            
        

class Logicstate():
    #A state should have at least three methods: handle its own events, update the game world, and draw something different on the screen
    def __init__(self, player = None):
        self.origin = [0,0]
        self.player = player

        self.keyup = False

        self.time_walk = 5

    """
    Main Loop
    """
    def event_listen(self):
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                quit()
                pygame.quit()

            if event.type == pygame.KEYUP:
                self.keyup = True
            else:
                self.keyup = False
            
        keys = pygame.key.get_pressed()
            
        if keys[K_DOWN] or keys[ord('s')]:
            self.player.mode = 'down'
            self.player.walking = True
        elif keys[K_RIGHT] or keys[ord('d')]:
            self.player.mode = 'right'
            self.player.walking = True
        elif keys[K_UP] or keys[ord('w')]:
            self.player.mode = 'up'
            self.player.walking = True
        elif keys[K_LEFT] or keys[ord('a')]:
            self.player.mode = 'left'
            self.player.walking = True

        if not keys[K_LEFT] and not keys[K_UP] and not keys[K_RIGHT] and not keys[K_DOWN]:
            if not keys[ord('s')] and not keys[ord('d')] and not keys[ord('w')] and not keys[ord('a')]:
                self.player.walking = False
            

        
    def update_logic_state(self):
        
        if self.player.walking:
            self.time_walk -= 1
            if self.time_walk < 0:
                
                self.player.step_animation()
                    
                self.time_walk = 5
            self.player.accelerate()
            self.player.update_position()
            

        else:
            self.player.sprite = player_anim_sprite[self.player.mode][1]
            self.player.velocity_x = 0
            self.player.velocity_y = 0
            

def main():
    pass
if __name__ == "__main__":
    main()
