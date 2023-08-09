import random

import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane,Obstacle
import numpy as np
import itertools

#class mei if we define smthg as self. then its a characteristic of self....but without self. it will just become a local variable
class Game:
    def __init__(self):

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird')
        self.clock = pygame.time.Clock()
        self.active = True
        self.episode = 0
        self.score_increase = False
        self.epsilon = 1  # Initial exploration probability
        self.epsilon_decay = 0.9997# Epsilon decay factor
        self.num_episodes = 20000

        #sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        #scale factor
        bg_height = pygame.image.load('../grapics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        #sprite setup
        BG(self.all_sprites,self.scale_factor)
        Ground([self.all_sprites,self.collision_sprites],self.scale_factor)
        self.plane = Plane(self.all_sprites,self.scale_factor/1.7)# to access the plane we did this...since its just a sprite in all sprites

        #timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer,1400)

        #text
        self.font = pygame.font.Font('../grapics/font/BD_Cartoon_Shout.ttf',30)
        self.score = 0

        #menu
        self.menu_surf = pygame.image.load('../grapics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH/2 ,WINDOW_HEIGHT/2))

        #music
        self.music = pygame.mixer.Sound('../sounds/sounds_music.wav')
        self.music.play(loops=-1)

        self.obstacle_list = []
    def collisions(self):
        if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False):
            if pygame.sprite.spritecollide(self.plane,self.collision_sprites,False,pygame.sprite.collide_mask):
                for sprite in self.collision_sprites.sprites():
                    if sprite.sprite_type == 'obstacle':
                        sprite.kill()
                self.active = False
                self.plane.kill()
                self.episode +=1
                self.epsilon *= self.epsilon_decay

        if self.plane.rect.top <=0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.plane.kill()
            self.episode +=1



    def display_score(self):
        if self.active:
            obstacles_to_remove = []
            for obstacle in self.obstacle_list:
                if obstacle.rect.right < self.plane.rect.x:
                    self.score += 1
                    print(self.obstacle_list.index(obstacle))
                    self.score_increase = True
                    obstacles_to_remove.append(obstacle)

            for obstacle in obstacles_to_remove:
                self.obstacle_list.remove(obstacle)



            y = WINDOW_HEIGHT/10

        else:
            y = WINDOW_HEIGHT/2 + self.menu_rect.height/1.5

        score_surf = self.font.render(str(self.score),True,'black')
        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH/2,y))

        self.display_surface.blit(score_surf,score_rect)

    def mrun(self):
        last_time = time.time()
        obstacle = 0
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                        self.score = 0
                        self.active = True
                        self.obstacle_list.clear()

                if event.type == self.obstacle_timer and self.active ==  True:
                    obstacle = Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)#to make the harder we multipied 1.1
                    self.obstacle_list.append(obstacle)






            # game logic
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()#important to keep this after draw since it overlaps

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf,self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)

    def get_state(self):
        if self.obstacle_list:
            latest_obstacle = self.obstacle_list[0]
            co_up = 0
            co_down = 0
            if latest_obstacle.orientation == 'up':
                co_up = latest_obstacle.rect.top
            else:
                co_down = latest_obstacle.rect.bottom


            return [self.plane.rect.y,co_up,co_down,latest_obstacle.rect.centerx]

        else:
            return [365, 0, 392, 431]


    def initialize_q_values(self):
        # Initialize Q-values with small random values to break the initial symmetry
        q_values = {}
        for tiles in self.get_all_combinations():
            for action in range(self.num_actions):
                q_values[tiles, action] = 0
        return q_values


    def get_all_combinations(self):
        all_possible_tiles = 0

        # Generate all possible tile combinations for all tilings
        total_tiling = []
        for i in range(self.num_tilings):
            tiling = []
            for a in range(self.tile_coder.bins[0]+2):
                for b in range(self.tile_coder.bins[0]+2):
                    for c in range(self.tile_coder.bins[0]+2):
                        for d in range(self.tile_coder.bins[0]+2):
                            tiling.append((a,b,c,d))
            total_tiling.append(tuple(tiling))

        total_tiling = tuple(total_tiling)
        print(total_tiling[0])
        all_possible_tiles = tuple(itertools.product(*total_tiling))
        return all_possible_tiles

    def RLrun(self):
        self.num_actions = 2
        self.num_tilings = 2
        bins = [8,8,8,8]
        offset = [-50,-50,-50,-50]
        self.tile_coder = TileCoder(self.num_tilings,bins,offset)
        alpha = 0.1  # Learning rate
        gamma = 0.9  # Discount factor

        self.q_table = self.initialize_q_values()
        #print(self.q_table)

        last_time = time.time()
        obstacle = 0
        action = 0
        state = 0
        initial_tiles = 0
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and (self.episode == 0 or self.episode>self.num_episodes):
                    if self.active:

                        #self.plane.jump()
                        pass
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                        self.score = 0
                        self.active = True
                elif self.episode > 0 and self.episode <=self.num_episodes:
                    if self.active:

                        #self.plane.jump()
                        pass
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.7)
                        self.score = 0
                        self.active = True
                        self.obstacle_list.clear()


                if event.type == self.obstacle_timer and self.active ==  True:
                    obstacle = Obstacle([self.all_sprites,self.collision_sprites],self.scale_factor * 1.1)#to make the harder we multipied 1.1
                    self.obstacle_list.append(obstacle)

            # game logic
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            #important to keep this after draw since it overlaps

            if self.active:
                if self.episode <=self.num_episodes:

                    #print(state)


                    if self.episode ==0:
                        state = self.get_state()
                        initial_tiles = self.tile_coder.get_tiles(state)
                        if random.random() < self.epsilon:
                            action = random.randint(0, self.num_actions - 1)  # Explore
                        else:
                            if self.q_table[initial_tiles,0] > self.q_table[initial_tiles,1]:
                                action = 0
                            else:
                                action = 1

                    reward = 0
                    if action == 0:
                        pass
                    else:
                        self.plane.jump()


                    self.score_increase = False
                    self.display_score()
                    self.collisions()

                    if self.active == False:
                        reward = -10
                    elif self.score_increase == True:
                        reward = 1
                    else:
                        reward = 0.1

                    state = self.get_state()
                    next_tiles = self.tile_coder.get_tiles(state)
                    next_action = 0
                    '''if self.q_table[next_tiles,0] > self.q_table[next_tiles,1]:
                        next_action = 0
                    else:
                        next_action = 1'''
                    if random.random() < self.epsilon:
                        next_action = random.randint(0, self.num_actions - 1)  # Explore
                    else:
                        if self.q_table[next_tiles,0] > self.q_table[next_tiles,1]:
                            next_action = 0
                        else:
                            next_action = 1
                    #print(next_action)
                    target = reward + gamma * self.q_table[next_tiles,next_action]
                    self.q_table[initial_tiles,action] += alpha * (target - self.q_table[initial_tiles,action])
                    self.epsilon *= self.epsilon_decay
                    action = next_action
                    initial_tiles = next_tiles


                else:
                    action = 0
                    state = self.get_state()
                    initial_tiles = self.tile_coder.get_tiles(state)
                    if self.q_table[initial_tiles, 0] > self.q_table[initial_tiles, 1]:
                        action = 0
                    else:
                        action = 1

                    if action == 0:
                        pass
                    else:
                        self.plane.jump()

                    self.display_score()
                    self.collisions()




            else:
                self.display_surface.blit(self.menu_surf,self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)

class TileCoder:
    def __init__(self, num_tilings, bins, offset):
        self.num_tilings = num_tilings
        self.bins = bins
        self.offset = offset

    def get_tiles(self, state):
        tiles = []
        for tiling in range(self.num_tilings):
            tiling_offset = [tiling * x for x in self.offset]
            tiling_tiles = []
            for i in range(len(state)):
                # Discretize the state value using tile width and offset
                if i==3:
                    a = 480/self.bins[i]
                else:
                    a = 800/self.bins[i]
                pos = int((state[i] - tiling_offset[i]) / a)
                if pos < 0:
                    pos = 0
                tiling_tiles.append(pos)
            tiles.append(tuple(tiling_tiles))
        return tuple(tiles)






if __name__ == '__main__':
    game = Game()
    run_method = input()
    if run_method == "mrun":# manual gameplay
        game.mrun()
    else:
        game.RLrun() # automatic gameplay
