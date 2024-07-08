import pygame as pg
import random as rand

# pygame setup


# GAME SETTINGS
SPEED = 6
UNIT = 40
WIDTH = 32
HEIGHT = 18

# pygame setup
pg.init()
screen = pg.display.set_mode((WIDTH*UNIT, HEIGHT*UNIT))
clock = pg.time.Clock()
running = True
alive = True
count = 0

direction = ""
temp = "E"
dico = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0), "": (0, 0)}

grid = [[' '] * WIDTH for _ in range(HEIGHT)]
grid[8][15], grid[8][14], grid[8][13] = 'S', 'S', 'S'
snake_dir = ["E", "E", "E"]
snake_pos = [pg.Vector2(15*UNIT, 8*UNIT), pg.Vector2(14*UNIT, 8*UNIT), pg.Vector2(13*UNIT, 8*UNIT)]
len_snake = 3
head_pos = [15, 8]
tail_pos = [13, 8]

apple_pos = [24, 8]


def get_direction(temp):
    keys = pg.key.get_pressed()
    if keys[pg.K_z] and direction != "S":
        temp = "N"
    elif keys[pg.K_s] and direction != "N":
        temp = "S"
    elif keys[pg.K_q] and direction != "E":
        temp = "W"
    elif keys[pg.K_d] and direction != "W":
        temp = "E"
    return temp


def new_apple(grille):
    x = rand.randint(0, WIDTH-1)
    y = rand.randint(0, HEIGHT-1)
    while grille[y][x] == 'S':
        x = rand.randint(0, WIDTH-1)
        y = rand.randint(0, HEIGHT-1)
    return [x, y]

def new_tail():
    snake_dir.append(snake_dir[-1])
    tail = snake_pos[-1]
    dx, dy = dico[snake_dir[-1]]
    snake_pos.append(pg.Vector2(tail.x-UNIT*dx, tail.y-UNIT*dy))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((20, 20, 30))

    # like a checkerboard
    for i_lig in range(HEIGHT):
        for i_col in range(WIDTH):
            if (i_lig+i_col)%2 == 0:
                pg.draw.rect(screen, (24, 24, 34), pg.Rect(i_col*UNIT, i_lig*UNIT, UNIT, UNIT))

    # draw snake
    for player_pos in snake_pos:
        pg.draw.rect(screen, "white", pg.Rect(player_pos, (UNIT, UNIT)))
    dx, dy = dico[snake_dir[0]]
    x = snake_pos[0].x + UNIT//4 + UNIT//8*dx + abs(UNIT//8*dx)
    y = snake_pos[0].y + UNIT//4 + UNIT//8*dy + abs(UNIT//8*dy)
    pg.draw.rect(screen, (20, 20, 30), pg.Rect(x, y, UNIT//4, UNIT//4))

    # draw apple
    pg.draw.rect(screen, (230, 50, 50), pg.Rect(apple_pos[0]*UNIT, apple_pos[1]*UNIT, UNIT, UNIT))

    # get key pressed
    temp = get_direction(temp)


    # change direction and detect collision
    if count%(60//SPEED) == 0:
        # each square get the next direction
        for i in range(1, len(snake_dir)):
            snake_dir[len_snake-i] = snake_dir[len_snake-i-1]
        direction = temp
        snake_dir[0] = direction

        # add the head
        head_pos[0] = (head_pos[0] + dico[direction][0])%WIDTH
        head_pos[1] = (head_pos[1] + dico[direction][1])%HEIGHT

        # collision
        if grid[head_pos[1]][head_pos[0]] == "S":
            alive = False
        grid[head_pos[1]][head_pos[0]] = "S"

        if head_pos[0] == apple_pos[0] and head_pos[1] == apple_pos[1]:
            apple_pos = new_apple(grid)
            new_tail()
            len_snake += 1
        else:
            # remove the tail
            grid[tail_pos[1]][tail_pos[0]] = " "
            tail_pos[0] = (tail_pos[0] + dico[snake_dir[-1]][0])%WIDTH
            tail_pos[1] = (tail_pos[1] + dico[snake_dir[-1]][1])%HEIGHT

    # animate each square
    for i in range(len(snake_pos)):
        i_direction = snake_dir[i]
        dx, dy = dico[i_direction]

        player_pos = snake_pos[i]

        # move the square
        player_pos.x += UNIT/60 * dx * SPEED
        player_pos.y += UNIT/60 * dy * SPEED

        # out of screen
        if player_pos.x >= WIDTH*UNIT:
            player_pos.x = 0
        elif player_pos.x <= -UNIT:
            player_pos.x = (WIDTH-1)*UNIT
        elif player_pos.y >= HEIGHT*UNIT:
            player_pos.y = 0
        elif player_pos.y <= -UNIT:
            player_pos.y = (HEIGHT-1)*UNIT
        

    # flip() the display to put your work on screen
    if alive:
        pg.display.flip()

    # limits FPS to 60
    clock.tick(60)
    count += 1

pg.quit()
