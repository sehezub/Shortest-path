import pygame
import math

def draw_square_from_coordinate(screen, pos, n):
    if pos[1] <= 25:
        return
    pygame.draw.rect(screen, (255,255,255), (math.floor(pos[0]/n)*n, math.floor(pos[1]/n)*n, n, n))

#just handling that the square size is ok
try:
    n = int(input('size of the square (grid is 800x600 and size must divide both):\n'))
    if 800 % n != 0 or 600 % n != 0:
        raise  ValueError
except (ValueError):
    while True:
        try:
            n = int(input('size must be an int dividing both 800 and 600, try again\n'))
            if 800 % n != 0 or 600 % n != 0:
                raise ValueError
            break
        except(ValueError):
            continue
pygame.init()

#n=10 #assert n\800,600
screen = pygame.display.set_mode(size=(800,625))

pygame.display.set_caption('Path finder')
pygame.draw.line(screen, (255,0,0), (0,25), (800,25))
#pygame.draw.rect(screen, (255,255,255), (0, 25, n, n))

draw_square_from_coordinate(screen, (0,25), n)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            raise SystemExit

    pygame.display.update()