import pygame
import math
import time

def save_and_draw(screen, n, buffer, pos):
    if buffer.count(pos) >= 1 or pos[1] <= 24:
        return buffer
    else:
        buffer.append(pos)
        pygame.draw.rect(screen, (255,255,255), (pos[0], pos[1], n, n))
        return buffer

def create_set_of_obst(states, n, s):
    for saves in states:
        for pos in saves:
            s.add((pos[0]//n, (pos[1]-25)//n))
            #print((pos[0]//n - pos[0]/n, (pos[1]-25)//n - (pos[1]-25)/n))
    return s


#just handling that the square size is ok
try:
    n = int(input('size of the square (grid is 800x600 and size must divide both):\n'))
    if 800 % n != 0 or 600 % n != 0:
        raise  ValueError
except (ValueError):
    while True:
        try:
            n = int(input('size must be an int dividing both 800 and 600, try again:\n'))
            if 800 % n != 0 or 600 % n != 0:
                raise ValueError
            break
        except(ValueError):
            continue
#

pygame.init()

states = list()
buffer = list()
obstacles = set() #set containing 2-tuples of the obstacles

is_hold_clicked = False

screen = pygame.display.set_mode(size=(800,625))
pygame.display.set_caption('Path finder')

pygame.draw.line(screen, (255,0,0), (0,24), (800,24))
pygame.draw.rect(screen, (0,255,0), (0, 0 , 40, 20))

#main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(create_set_of_obst(states, n, obstacles))
            raise SystemExit

        if is_hold_clicked:
            buffer = save_and_draw(screen, n, buffer, (math.floor(pygame.mouse.get_pos()[0]/n)*n, 25+(math.floor((pygame.mouse.get_pos()[1]-25)/n))*n))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[0] <= 40 and pygame.mouse.get_pos()[1] <= 20 and states != []:
                for pos in states[-1]:
                    pygame.draw.rect(screen, (0, 0, 0), (pos[0], pos[1], n, n))
                del states[-1]

                for saves in states:
                    for pos in saves:
                        pygame.draw.rect(screen, (255, 255, 255), (pos[0], pos[1], n, n))
            else:
                is_hold_clicked = True
                buffer = save_and_draw(screen, n, buffer, (math.floor(pygame.mouse.get_pos()[0]/n)*n, 25+(math.floor((pygame.mouse.get_pos()[1]-25)/n))*n))

        if event.type == pygame.MOUSEBUTTONUP:
            is_hold_clicked = False
            if buffer != []:
                states.append(buffer.copy())
                buffer.clear()

    pygame.display.update()