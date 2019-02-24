import pygame
import random

#settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)


class playerBlock(pygame.sprite.Sprite):
    def __init__(self,width,height,speed,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width,height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.width = width
        self.height = height
        self.speed = speed
        self.shootCD = 15

    def setSpeed(self,speed):
        self.speed = speed
    def setColor(self,color):
        self.color = color
    def setCenter(self,x,y):
        self.rect.center = (x,y)

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keystate[pygame.K_RIGHT]:
            self.rect.x += self.speed

        #stop moving off screen
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx,self.rect.top)
        gamesprites.add(bullet)
        bullets.add(bullet)

class enemyBlock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 30
        self. height = 30
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH-self.rect.width)
        self.rect.y = random.randrange(-200,-30)
        self.speedy = random.randrange(6,12)
        self.speedx = random.randrange(0,5)

    def setSpeed(self,speed):
        self.speed = speed
    def setColor(self,color):
        self.image.fill(color)
    def setCenter(self,x,y):
        self.rect.center = (x,y)
    def reset(self):
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-90, -30)
        self.speedy = random.randrange(2, 10)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > SCREEN_HEIGHT + 5:
            self.reset()
        if self.rect.x < 0:
            self.speedx = -self.speedx
        if self.rect.x > SCREEN_WIDTH-self.width:
            self.speedx = -self.speedx

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        self.speedy = 15
        self.width = 5
        self.height = 10
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.y -= self.speedy
        #remove bullet, if its out of bounds
        if self.rect.bottom <0:
            self.kill()


#initialize game
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("blockGame")
clock = pygame.time.Clock()

gamesprites = pygame.sprite.Group()
enemySprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = playerBlock(50,50,10,GREEN)
player.setCenter(SCREEN_WIDTH/2,SCREEN_HEIGHT-50)
gamesprites.add(player)

for i in range(0,10):
    enemy = enemyBlock()
    gamesprites.add(enemy)
    enemySprites.add(enemy)

def gameLoop():
    running = True

    while running:
        #keep fps
        clock.tick(FPS)

        #process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.shootCD <= 0:
                    player.shoot()
                    player.shootCD = 15
        #update
        player.shootCD -= 1
        gamesprites.update()

        #check collision between player and enemies

        bodyHits = pygame.sprite.spritecollide(player,enemySprites,False)
        playerBulletHits = pygame.sprite.groupcollide(enemySprites,bullets,True,True)
        for hit in playerBulletHits:
            enemy = enemyBlock()
            gamesprites.add(enemy)
            enemySprites.add(enemy)


        if bodyHits:
            running = False

        #DRAW
        screen.fill(BLACK)
        gamesprites.draw(screen)
        pygame.display.update()

    pygame.quit()
gameLoop()