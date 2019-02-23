import pygame

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




def main():

    #initialize game
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("blockGame")
    clock = pygame.time.Clock()

    gamesprites = pygame.sprite.Group()
    player = playerBlock(50,50,10,GREEN)
    player.setCenter(SCREEN_WIDTH/2,SCREEN_HEIGHT-50)
    gamesprites.add(player)

    #gameloop
    running = True

    while running:
        #keep fps
        clock.tick(FPS)

        #process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #update

        gamesprites.update()

        #DRAW
        screen.fill(BLACK)
        gamesprites.draw(screen)
        pygame.display.update()

    pygame.quit()
main()