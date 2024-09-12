import pygame
import math
import time
#paint only if is not in stack
#when removing from stack and painting verify is not in nodes_consideres

def least_cost_node(nodes_and_vals, visited_nodes, start):
    node = (())
    for j in iter(nodes_and_vals):
        if not j in visited_nodes and j != start:
            if node == (()): node = (j, nodes_and_vals[j][1])
            elif nodes_and_vals[j][1] <= node[1]\
                and abs(goal[0] - j[0]) + abs(goal[1] - j[1]) < abs(goal[0] - node[0][0]) + abs(goal[1] - node[0][1]):
                node = (j, nodes_and_vals[j][1])

    return node

def update_neighbour_nodes_and_draw(node, obstacles, goal, nodes, screen, start, visited):

    for j in [(node[0] - 1, node[1]), (node[0], node[1] + 1), (node[0] + 1, node[1]), (node[0], node[1] - 1)]:
            if j[0] < 0 or j[0] > 800//n - 1 or j[1] < 0 or j[1] > 600//n - 1 or j in obstacles or j == start:
                continue
            elif not j in nodes:
                pygame.draw.rect(screen, (110, 110, 110), (j[0] * n, (j[1] * n) + 25, n, n))
                nodes.update({ j: (nodes[node][0] + [node], len(nodes[node][0]) + abs(goal[0] - j[0]) + abs(goal[1] - j[1]))})
            elif len(nodes[node][0]) + abs(goal[0] - j[0]) + abs(goal[1] - j[1]) < nodes[j][1]:
                if not j in visited: pygame.draw.rect(screen, (110, 110, 110), (j[0] * n, (j[1] * n) + 25, n, n))
                nodes.update({ j: (nodes[node][0] + [node], len(nodes[node][0]) + abs(goal[0] - j[0]) + abs(goal[1] - j[1]))})
    return

def save_and_draw(screen, n, buffer, pos):
    if buffer.count(pos) >= 1 or pos[1] <= 24:
        return buffer
    else:
        buffer.append(pos)
        pygame.draw.rect(screen, (255,255,255), (pos[0], pos[1], n, n))
        return buffer

def create_set_of_obst(states, n):
    s = set()
    for saves in states:
        for pos in saves:
            s.add((pos[0]//n, (pos[1]-25)//n))
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
path = []
nodes_and_val = dict()
visited_nodes = set()
obstacles = set() #set containing 2-tuples of the obstacles
goal = ()
start = ()
delay = 0.005

start_rect = pygame.Rect((250, 0), (24, 24))
goal_rect = pygame.Rect((500, 0), (24, 24))
return_rect = pygame.Rect((0, 0), (40, 20))
run_rect = pygame.Rect((775,0), (24, 24))
speed1_rect = pygame.Rect((350,0), (24, 24))
speed2_rect = pygame.Rect((375,0), (24, 24))
speed3_rect = pygame.Rect((400,0), (24, 24))

is_click_hold = False
set_start = False
set_goal = False
is_running = False
finished = False
path_printed = False

screen = pygame.display.set_mode(size=(800,625))
pygame.display.set_caption('Path finder')

pygame.draw.line(screen, (255,0,0), (0,24), (800,24))

pygame.draw.line(screen, (255,255,255), (0,10), (40,10), width=3)
pygame.draw.line(screen, (255,255,255), (0,10), (15,17), width=3)
pygame.draw.line(screen, (255,255,255), (0,10), (15,3), width=3)

pygame.draw.rect(screen, (0,255,0), start_rect) #start button
pygame.draw.rect(screen, (255,0,0), goal_rect) #goal button
pygame.draw.rect(screen, (115,80,120), speed1_rect)
#pygame.draw.rect(screen, (95,60,100), speed2_rect)
pygame.draw.rect(screen, (75,40,80), speed3_rect)

pygame.draw.circle(screen, (50,50,255), (787,12), 12, width=3) #run button

#main loop
while True:
    if is_running:

        if path_printed:
            time.sleep(0.1)

        elif finished:
            pygame.draw.rect(screen, (50, 50, 255), (path[0][0] * n, (path[0][1] * n) + 25, n, n))
            time.sleep(delay)
            pygame.display.update()
            del path[0]
            if path == []: path_printed = True

        else:
            time.sleep(delay)
            n_node = least_cost_node(nodes_and_val, visited_nodes, start)

            if n_node == (()): finished, path_printed = True, True #no path
            else:
                visited_nodes.add(n_node[0])
                pygame.draw.rect(screen, (math.floor(255 * ( nodes_and_val[n_node[0]][1] - abs(n_node[0][0] - goal[0]) - abs(n_node[0][1] - goal[1])) / nodes_and_val[n_node[0]][1]), math.floor(255 * (1 - (nodes_and_val[n_node[0]][1] - abs(n_node[0][0] - goal[0]) - abs(n_node[0][1] - goal[1])) / nodes_and_val[n_node[0]][1])), 0), (n_node[0][0] * n, (n_node[0][1] * n) + 25, n, n))
                if abs(n_node[0][0] - goal[0]) + abs(n_node[0][1] - goal[1]) == 1:
                    finished = True
                    path = nodes_and_val[n_node[0]][0][2:] + [n_node[0]]
                    #for j in nodes_and_val[n_node[0]][0][2:] + [n_node[0]]:
                    #    pygame.draw.rect(screen, (50,50,255), (j[0] * n, (j[1] * n) + 25, n, n))
                    #    time.sleep(delay)
                    #    pygame.display.update()
                else:
                    update_neighbour_nodes_and_draw(n_node[0], obstacles, goal, nodes_and_val, screen, start, visited_nodes)

    else:
        time.sleep(0.007)

    for event in pygame.event.get():

        if event.type == pygame.QUIT: raise SystemExit

        pos = pygame.mouse.get_pos()

        if is_click_hold and  (math.floor(pos[0]/n)*n, 25+(math.floor((pos[1]-25)/n))*n) != goal\
                and (math.floor(pos[0]/n)*n, 25+(math.floor((pos[1]-25)/n))*n) != start\
                and not is_running:
            buffer = save_and_draw(screen, n, buffer, (math.floor(pos[0]/n)*n, 25+(math.floor((pos[1]-25)/n))*n))

        if event.type == pygame.MOUSEBUTTONDOWN:

            if speed1_rect.collidepoint(pos):
                delay = 0.1
                pygame.draw.rect(screen, (0, 0, 0), speed1_rect)
                pygame.draw.rect(screen, (95, 60, 100), speed2_rect)
                pygame.draw.rect(screen, (75, 40, 80), speed3_rect)

            elif speed2_rect.collidepoint(pos):
                delay = 0.005
                pygame.draw.rect(screen, (115, 80, 120), speed1_rect)
                pygame.draw.rect(screen, (0, 0, 0), speed2_rect)
                pygame.draw.rect(screen, (75, 40, 80), speed3_rect)

            elif speed3_rect.collidepoint(pos):
                delay = 0
                pygame.draw.rect(screen, (115, 80, 120), speed1_rect)
                pygame.draw.rect(screen, (95, 60, 100), speed2_rect)
                pygame.draw.rect(screen, (0, 0, 0), speed3_rect)

            if not is_running:

                if pos[1] >= 25:

                    if not set_goal and not set_start\
                            and (math.floor(pos[0] / n) * n,
                                 25 + (math.floor((pos[1] - 25) / n)) * n) != goal \
                            and (math.floor(pos[0] / n) * n,
                                 25 + (math.floor((pos[1] - 25) / n)) * n) != start:
                        is_click_hold = True
                        buffer = save_and_draw(screen, n, buffer, (math.floor(pos[0] / n) * n, 25 + (
                            math.floor((pos[1] - 25) / n)) * n))

                    elif set_goal and not any((math.floor(pos[0]/n)*n, 25+(math.floor((pos[1]-25)/n))*n) in saves for saves in states)\
                            and (math.floor(pos[0]/n)*n, 25+(math.floor((pos[1]-25)/n))*n) != start:
                        if goal != ():
                            pygame.draw.rect(screen, (0, 0, 0), (goal[0], goal[1], n, n))
                        goal = (math.floor(pos[0]/n)*n, 25+(math.floor((pos[1]-25)/n))*n)
                        set_goal = False
                        pygame.draw.rect(screen, (255,0,0), (goal[0], goal[1], n, n))

                    elif set_start and not any((math.floor(pos[0]/n)*n, 25+(math.floor((pos[1]-25)/n))*n) in saves for saves in states)\
                            and (math.floor(pos[0]/n)*n, 25+(math.floor((pos[1]-25)/n))*n) != goal :
                        if start != ():
                            pygame.draw.rect(screen, (0, 0, 0), (start[0], start[1], n, n))
                        start = (math.floor(pos[0]/n)*n, 25+(math.floor((pos[1]-25)/n))*n)
                        set_start = False
                        pygame.draw.rect(screen, (0,255,0), (start[0], start[1], n, n))

                elif return_rect.collidepoint(pos) and states != []:
                    for pos in states[-1]:
                        pygame.draw.rect(screen, (0, 0, 0), (pos[0], pos[1], n, n))
                    del states[-1]

                    for saves in states:
                        for pos in saves:
                            pygame.draw.rect(screen, (255, 255, 255), (pos[0], pos[1], n, n))

                elif start_rect.collidepoint(pos):
                    set_start = True
                    set_goal = False

                elif goal_rect.collidepoint(pos):
                    set_goal = True
                    set_start = False

                elif run_rect.collidepoint(pos) and goal != () and start != ():
                    is_running = True
                    set_goal = False
                    set_start = False
                    pygame.draw.rect(screen, (0, 0, 0), run_rect)
                    pygame.draw.line(screen, (50,50,255), (775, 0), (798, 21), width=4)
                    pygame.draw.line(screen, (50,50,255), (775, 21), (798, 0), width=4)
                    #start running
                    obstacles = create_set_of_obst(states, n)
                    goal = (goal[0]//n, (goal[1]-25)//n)
                    start = (start[0]//n, (start[1]-25)//n)
                    nodes_and_val.update({start: ([start], abs(start[0] - goal[0]) + abs(start[1] - goal[1]))})

                    if abs(goal[0] - start[0]) + abs(goal[1] - start[1]) == 1:
                        finished = True
                        path_printed = True

                    else:
                        nodes_and_val.update({start: ([start], abs(start[0] - goal[0]) + abs(start[1] - goal[1]))})
                        update_neighbour_nodes_and_draw(start, obstacles, goal, nodes_and_val, screen, start, visited_nodes)

            elif run_rect.collidepoint(pos):
                is_running = False
                finished = False
                path_printed = False
                pygame.draw.rect(screen, (0,0,0), run_rect)
                pygame.draw.circle(screen, (50,50,255), (787, 12), 12, width=3)
                #stop running
                del nodes_and_val[start]
                goal = (goal[0] * n, (goal[1] * n) + 25)
                start = (start[0] * n, (start[1] * n) + 25)
                obstacles.clear()
                visited_nodes.clear()
                path.clear()

                for j in iter(nodes_and_val):
                    pygame.draw.rect(screen, (0, 0, 0), (j[0] * n, (j[1] * n) + 25, n, n))
                nodes_and_val.clear()

        elif event.type == pygame.MOUSEBUTTONUP:
            is_click_hold = False
            if buffer != []:
                states.append(buffer.copy())
                buffer.clear()

    pygame.display.update()