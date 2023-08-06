import pygame
from settings import *
from random import choice,randint
class BG(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        bg_image = pygame.image.load('../grapics/environment/background.png').convert_alpha()

        full_height = bg_image.get_height() * scale_factor
        full_width = bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(bg_image,(full_width,full_height))

        self.image = pygame.Surface((full_width*2,full_height))
        self.image.blit(full_sized_image,(0,0))
        self.image.blit(full_sized_image,(full_width,0))

        self.rect = self.image.get_rect(topleft = (0,0))
        self.pos = pygame.math.Vector2(self.rect.topleft)#explained in delta time the need for this

    def update(self,dt):
        self.pos.x -= 300 * dt #explained in dt time video the need for this to get consistent movement with different frame rates
        if self.rect.centerx < 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Ground(pygame.sprite.Sprite):
    #we have already scaled the image instead of taking two images side by side as in BG since we need to do collision
    def __init__(self,groups,scale_factor): #to maintain consistency we need to mulitply every image
        super().__init__(groups)

        self.sprite_type = 'ground'

        #image
        ground_surf = pygame.image.load('../grapics/environment/ground.png').convert_alpha()
        #combined the 3 lines of code which i wrote for class bg
        self.image = pygame.transform.scale(ground_surf,pygame.math.Vector2(ground_surf.get_size()) * scale_factor)

        #postion
        self.rect = self.image.get_rect(bottomleft = (0,WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Plane(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)

        #image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]


        #rect
        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH/20,WINDOW_HEIGHT/2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        #movement
        self.gravity = 800
        self.direction = 0

        #mask
        self.mask = pygame.mask.from_surface(self.image)

        #sound
        self.jump_sound = pygame.mixer.Sound('../sounds/sounds_jump.wav')
        self.jump_sound.set_volume(0.3)


    def import_frames(self,scale_factor):
        self.frames = []
        for i in range(3):
            surf = pygame.image.load(f'../grapics/plane/red{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size())* scale_factor)
            self.frames.append(scaled_surface)

    def applygravity(self,dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        self.jump_sound.play()
        self.direction = -400

    def animate(self,dt):
        self.frame_index += 10 *dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image,-self.direction * 0.06 ,1) # self direciton was very large
        #we dont rotate anything by itself, we are just rotating wrt direction..so since no movement as such..no dt required
        self.image = rotated_plane
        # mask
        #since we are changing the actual image/surf itself we need to update the mask everytime
        #in obstacle and ground, the surf remains same and we just update the rect everytime hence the mask for it can be given in init
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.applygravity(dt)
        self.animate(dt) # animate must come before rotate..since we are overwriting the image
        self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,groups,scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obstacle'

        self.orientation = choice(('up','down'))
        surf = pygame.image.load(f'../grapics/obstacles/{choice((0,1))}.png').convert_alpha()
        self.image = pygame.transform.scale(surf,pygame.math.Vector2(surf.get_size())* scale_factor)



        x = WINDOW_WIDTH + randint(40,60)
        if self.orientation == 'up':
            y= WINDOW_HEIGHT + randint(10,50)
            self.rect = self.image.get_rect(midbottom = (x,y) )
        else:
            y = randint(-50,-10)
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect = self.image.get_rect(midtop = (x,y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

        # mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.pos.x -= 400 *dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= 0:
            self.kill()









