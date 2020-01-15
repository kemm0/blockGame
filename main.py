import pygame
import os
import random

"""
  _     _            _     _____                      
 | |   | |          | |   / ____|                     
 | |__ | | ___   ___| | _| |  __  __ _ _ __ ___   ___ 
 | '_ \| |/ _ \ / __| |/ / | |_ |/ _` | '_ ` _ \ / _ \
 | |_) | | (_) | (__|   <| |__| | (_| | | | | | |  __/
 |_.__/|_|\___/ \___|_|\_\\_____|\__,_|_| |_| |_|\___|
                                                      
                                                      

A 2d shoot-em-up type game. 
Author: Juho Keto-Tokoi (kemm0 on gitHub)
Music by: joshuaempyre https://freesound.org/people/joshuaempyre/

Game instructions:

Dodge and shoot the purple enemies. You get points based on the amount of enemies you shoot.
If you crash with an enemy or get hit by their bullets three times, you die.
Everytime you kill and enemy, a new one spawns and it will be a little bit faster.

Keybinds:
w = up
a = left
s = down
d = right
spacebar = shoot

TO-DO:

game menu
highscores / leaderboards
progressive difficulty based on the amount of points
"""

#settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 576
FPS = 30
os.environ['SDL_VIDEO_CENTERED'] = '1' #set gamescreen in the middle of computer screen

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,165,0)
PURPLE = (128,0,128)

PROGRESSIVE_DIFFICULTY = 1.5

#these are for upcoming gamemenu
GAMEMENU = 1
GAMELOOP = 2

"""
Class for player characters in the game
"""
class playerBlock(pygame.sprite.Sprite):
    def __init__(self,width,height,speed,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.speed = speed
        self.shootCD = 5
        self.points = 0
        self.health = 3

    def setSpeed(self,speed):
        self.speed = speed
    def setColor(self,color):
        self.color = color
    def setCenter(self,x,y):
        self.rect.center = (x,y)
    def hit(self):  # make player change color based on health level
        self.health -= 1
        if(self.health == 2):
            self.image.fill(YELLOW)
        if(self.health == 1):
            self.image.fill(RED)

    """
    Updates the player's position based on keys that have been pressed. Checks screen boundaries, so that player
    doesn't move off screen.
    
    return: None
    """
    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keystate[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keystate[pygame.K_UP]:
            self.rect.y -= self.speed
        if keystate[pygame.K_DOWN]:
            self.rect.y += self.speed

        #stop moving off screen
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    """
    creates a new bullet and adds it to the list of sprites
    
    return: None
    """
    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top,-15)
        gamesprites.add(bullet)
        playerBullets.add(bullet)

class enemyBlock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 30
        self. height = 30
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH-self.rect.width)
        self.rect.y = random.randrange(-200,-30)
        self.speedy = random.randrange(2,6)
        self.speedx = random.randrange(-2,2)
        self.shootProp = random.randrange(1,10)
        self.shootCD = 20

    def setSpeed(self,speed):
        self.speed = speed
    def setColor(self,color):
        self.image.fill(color)
    def setCenter(self,x,y):
        self.rect.center = (x,y)

    """
    Resets the enemyBlock's location, y-axis speed, x-axis speed and shooting propability.
    These are pseudo-random values.
    
    Return :None
    """
    def reset(self):
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-90, -30)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-5, 5)
        self.shootProp = random.randrange(1,10)

    """
    Checks if the enemy is in boundaries of the screen. If it collides with the sides, it changes direction. If it's 
    below screen, it resets back up
    """
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > SCREEN_HEIGHT + 5:
            self.reset()
        if self.rect.x < 0:
            self.speedx = -self.speedx
        if self.rect.x > SCREEN_WIDTH-self.width:
            self.speedx = -self.speedx

    """
    creates a new bullet and adds it to the lists of sprites
    
    return: None
    """
    def shoot(self):
        shootingPropability = random.randrange(1,10)
        if shootingPropability == self.shootProp:
            bullet = Bullet(self.rect.centerx,self.rect.bottom,20,WHITE)
            enemyBullets.add(bullet)
            gamesprites.add(bullet)

"""
Bullet class, that's used by players and enemies.
"""
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,speed,color = BLUE):
        self.speedy = speed
        self.width = 10
        self.height = 10
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.color = color

    """
    moves the bullet with the amount of bullet's speed variable. If it's out of bounds, it gets deleted.
    """
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

def DisplayGameText(text,fontname,size,x,y,color = WHITE):
    messageFont = pygame.font.SysFont(fontname,size)
    message = messageFont.render(text,True,color)
    screen.blit(message,(x,y))


#initialize game

pygame.mixer.init(44100)
pygame.mixer.music.load("Sounds/gameMusic2.wav")
pygame.mixer.music.play(-1)

playerHitSound = pygame.mixer.Sound("Sounds/hit-sound1.ogg")

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("blockGame")
gameIcon = pygame.image.load("Images/gameIcon.png")
pygame.display.set_icon(gameIcon)
clock = pygame.time.Clock()
enemyCount = 6

gamesprites = pygame.sprite.Group()
enemySprites = pygame.sprite.Group()
playerBullets = pygame.sprite.Group()
enemyBullets = pygame.sprite.Group()
playersprites = pygame.sprite.Group()

player = playerBlock(50,50,10,GREEN)
player.setCenter(SCREEN_WIDTH/2,SCREEN_HEIGHT-50)
gamesprites.add(player)
playersprites.add(player)

# Create enemyCount amount of enemies and add them to the lists of sprites
for i in range(0,enemyCount):
    enemy = enemyBlock()
    gamesprites.add(enemy)
    enemySprites.add(enemy)


"""
The Loop for the actual game. Everything that happens in the actual game happens in this loop.

return: None
"""
def gameLoop():
    running = True
    gameOver = False

    while running:
        #keep fps
        clock.tick(FPS)

        #process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.shootCD <= 0 and player.health >0:
                    player.shoot()
                    player.shootCD = 5

        #update everything
        player.shootCD -= 1
        for enemy in enemySprites:
            enemy.shootCD -= 1
            if enemy.shootCD < 0:
                enemy.shoot()
                enemy.shootCD = 10

        gamesprites.update()

        #check collision between player and enemies

        bodyHits = pygame.sprite.spritecollide(player,enemySprites,True)
        playerBulletHits = pygame.sprite.groupcollide(enemySprites,playerBullets,True,True)
        enemyBulletHits = pygame.sprite.groupcollide(playersprites,enemyBullets,False,True)

        for hit in playerBulletHits:
            player.points += 1
            enemy = enemyBlock()
            enemy.speedx += PROGRESSIVE_DIFFICULTY * player.points * 0.1
            enemy.speedy += PROGRESSIVE_DIFFICULTY * player.points * 0.1
            gamesprites.add(enemy)
            enemySprites.add(enemy)

        for hit in enemyBulletHits:
            playerHitSound.play()
            player.hit()
        for hit in bodyHits:
            player.hit()
        if (player.health <= 0):
            player.kill()


        if(len(playersprites) == 0):
            gameOver = True

        #DRAW everything
        screen.fill(BLACK)
        gamesprites.draw(screen)
        DisplayGameText("Points: {}".format(player.points),"comicsansms",30,20,20)
        if(gameOver):
            DisplayGameText("YOU ARE DEAD","comicsansms",60,SCREEN_WIDTH/2-250,SCREEN_HEIGHT/2)
        pygame.display.update()

gameLoop()
pygame.quit()
quit()
