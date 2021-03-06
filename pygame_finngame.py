import pygame
import sys
import os

'''OBJECTS'''
#PUT CLASSES & FUNCTIONS HERE

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.momentumX = 0 #move along X
        self.momentumY = 0 #move along Y
        
        self.collide_delta = 0
        self.jump_delta = 6
        self.images = [ ]
        img = pygame.image.load(os.path.join('images', 'hero.png')).convert()
        self.images.append(img)

        self.image = self.images[0]
        self.rect = self.image.get_rect()
       


        self.image.convert_alpha() #optimise for alpha
        self.image.set_colorkey(alpha) #set alpha
        self.score = 0 #set score
    def control(self, x, y):
        #control player movement
        self.momentumX += x
        self.momentumY += y

    def gravity(self):
        self.momentumY += 3.2 #how fast player falls

        if self.rect.y > 960 and self.momentumY >= 0:
            self.momentumY = 0
            self.rect.y = screenY-20

    
    def jump (self, platform_list):
        self.jump_delta = 0
    def update(self, enemy_list, platform_list):
        #update sprite position
        currentX = self.rect.x
        nextX = currentX + self.momentumX
        self.rect.x = nextX

        currentY = self.rect.y
        nextY = currentY + self.momentumY
        self.rect.y = nextY

        #gravity
          

        #collisions
        block_hit_list = pygame.sprite.spritecollide(self, platform_list, False)
        if self.momentumX > 0:
             for block in block_hit_list:
                 self.rect.y = currentY
                 self.rect.x = currentX+9
                 self.momentumY = 0
                 self.collide_delta = 0 #stop jumping
                 
        if self.momentumY > 0:
             for block in block_hit_list:
                 self.rect.y = currentY
                 self.momentumY = 0
                 self.collide_delta = 0 #stop jumping

        enemy_hit_list = pygame.sprite.spritecollide(self, enemy_list, False)
        for enemy in enemy_hit_list:
            self.score -= 1
            print(self.score)

        if self.collide_delta < 6 and self.jump_delta < 6:
            self.jump_delta = 6*2
            self.momentumY -=33 #how high jump

            self.collide_delta +=6
            self.jump_delta += 6

class Platform(pygame.sprite.Sprite):
    #x (location, y location, img width, img height, img file)
    def __init__(self,xloc,yloc,imgw, imgh, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([imgw, imgh])
        self.image.convert_alpha()
        self.image.set_colorkey(alpha)
        self.blockpic = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc

        #paint image into blocks
        self.image.blit(self.blockpic, (0,0),(0,0,imgw,imgh))


    def level1():
        #create level 1
        platform_list = pygame.sprite.Group()
        block = Platform(0, 670,180, 31,os.path.join('images','platform.png'))
        platform_list.add(block) #after each block

        block = Platform(180, 670,180, 31,os.path.join('images','platform.png'))
        platform_list.add(block) #after each block

        block = Platform(360, 670,180, 31,os.path.join('images','platform.png'))
        platform_list.add(block) #after each block

        block = Platform(540, 670,180, 31,os.path.join('images','platform.png'))
        platform_list.add(block) #after each block

        block = Platform(720, 670,180, 31,os.path.join('images','platform.png'))
        platform_list.add(block) #after each block

        return platform_list #at end of function level11
        

class Enemy(pygame.sprite.Sprite):
    #spawn ana enemy
    def __init__(self,x,y,img): 
        pygame.sprite.Sprite.__init__(self)
        self.image= pygame.image.load(os.path.join('images', img))
        self.image.convert_alpha()
        self.image.set_colorkey(alpha)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0 #counter variable
    def move(self):
        #enemy movement
        if self.counter >= 0 and self.counter <= 30:
            self.rect.x += 2
        elif self.counter >= 30 and self.counter <= 60:
            self.rect.x -= 2
        else:
            self.counter = 0
            print('reset')

        self.counter +=1


       
'''SETUP'''
#CODE RUNS ONCE

screenX = 960 #width
screenY = 720 #height
alpha = (0, 0, 0)
black = (1, 1, 1)
white = (255, 255, 255)
fps = 40
afps = 4 #animation cycles
clock = pygame.time.Clock()
pygame.init()

main = True


screen = pygame.display.set_mode([screenX, screenY])
backdrop = pygame.image.load(os.path.join('images','backround.png')).convert()
backdropRect = screen.get_rect()
platform_list = Platform.level1()

player = Player() #Spawn
player.rect.x = 0
player.rect.y = 0
movingsprites = pygame.sprite.Group()
movingsprites.add(player)
movesteps = 10 #how fast move

forwardX = 600 #when to scroll
backwardX = 150 #when to scroll

#enemy code
enemy = Enemy(0,660,'Finn_enemy.png') #spawn enemy
enemy_list = pygame.sprite.Group() #create enemy group
enemy_list.add(enemy) #add enemy to group
                

'''MAIN LOOP'''
while main == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            main = False

        if event.type == pygame.KEYUP:
            if event.key == ord('q'):
                pygame.quit()
                sys.exit()
                main = False

            if event.key == pygame.K_LEFT:
                print('left stop')
                player.control(movesteps, 0)
            if event.key == pygame.K_RIGHT:
                print('right stop')
                player.control(-movesteps, 0)
            if event.key == pygame.K_UP:
                print('up stop')
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('left')
                player.control(-movesteps, 0)
            if event.key == pygame.K_RIGHT:
                print('right')
                player.control(movesteps, 0)
            if event.key == pygame.K_UP:
                print('up')
                player.jump(platform_list)

    #scroll world forward
    if player.rect.x >= forwardX:
         scroll = player.rect.x - forwardX
         player.rect.x = forwardX
         for platform in platform_list:
             platform.rect.x -= scroll

         for enemy in enemy_list:
              enemy.rect.x -= scroll



    #scroll world backward
    if player.rect.x <= backwardX:
         scroll = min(1, (backwardX - player.rect.x))
         player.rect.x = backwardX
         for platform in platform_list:
             platform.rect.x += scroll

         for enemy in enemy_list:
              enemy.rect.x += scroll
              
   
    screen.blit(backdrop, backdropRect)
    platform_list.draw(screen)
    player.gravity() #check gravity
    
    player.update(enemy_list, platform_list) #update player 
    movingsprites.draw(screen)  #draw player
    enemy.move() #move enemy sprite

    enemy_list.draw(screen) #refresh enemies


    pygame.display.flip()
    clock.tick(fps)

    








