import pygame
import math
import time

def save_and_draw(screen, n, buffer, pos):
    if buffer.count(pos) >= 1:
        return buffer
    else:
        buffer.append(pos)
        draw_square_from_coordinate(screen, pos, n, (255,255,255))
        return buffer

def draw_square_from_coordinate(screen, pos, n, color):
    if pos[1] <= 24:
        return
    pygame.draw.rect(screen, color, (math.floor(pos[0]/n)*n, 25+(math.floor((pos[1]-25)/n))*n, n, n))

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
#

pygame.init()

states = list()
buffer = list()
is_hold_clicked = False

screen = pygame.display.set_mode(size=(800,625))
pygame.display.set_caption('Path finder')

pygame.draw.line(screen, (255,0,0), (0,24), (800,24))
pygame.draw.rect(screen, (0,255,0), (0, 0 , 40, 20))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            i = 0
            for e in states:
                i = i + len(e)
            print(i)
            raise SystemExit

        if is_hold_clicked:
            buffer = save_and_draw(screen, n, buffer, pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos()[0] <= 40 and pygame.mouse.get_pos()[1] <= 20 and states != []:
                for pos in states[-1]:
                    draw_square_from_coordinate(screen, pos, n, (0,0,0))
                del states[-1]
            else:
                is_hold_clicked = True
                #print(pygame.mouse.get_pos())
                buffer = save_and_draw(screen, n, buffer, pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            is_hold_clicked = False
            if buffer != []:
                states.append(buffer.copy())
                buffer.clear()

    pygame.display.update()