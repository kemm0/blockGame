import pygame

class Block:
    def __init__(self,width,height):
        self.__width = width
        self.__height = height
        self.__speed = 2

def main():
    pygame.init()
    screen = pygame.display.set_mode((300,300))
    sprites = []
    WHITE = (255,255,255)
    playerBlock = pygame.draw.rect(screen,WHITE,(125,125,50,50))



    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_w):
                    playerBlock.move(0,-2)

        pygame.display.update()
main()