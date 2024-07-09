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
surface = pg.Surface((WIDTH*UNIT, HEIGHT*UNIT), pg.SRCALPHA)
clock = pg.time.Clock()
running = True
alive = True
count = 0

# movement setup
direction = ""
temp_direction = "E"
dico = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0), "": (0, 0)}

# create the snake and a grid
grid = [[' '] * WIDTH for _ in range(HEIGHT)]
grid[8][15], grid[8][14], grid[8][13] = 'S', 'S', 'S'
snake_dir = ["E", "E", "E"]
snake_pos = [pg.Vector2(15*UNIT, 8*UNIT), pg.Vector2(14*UNIT, 8*UNIT), pg.Vector2(13*UNIT, 8*UNIT)]
len_snake = 3
head_pos = [15, 8]
tail_pos = [13, 8]

# create an apple
apple_pos = [24, 8]


def get_direction(temp):
    keys = pg.key.get_pressed()
    # pause the game
    if keys[pg.K_ESCAPE]:
        pause_screen()
        return temp
    # change direction
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
    # generate a new apple position (not on the snake)
    while True:
        x = rand.randint(0, WIDTH-1)
        y = rand.randint(0, HEIGHT-1)
        if grille[y][x] == 'S':
            return [x, y]

def new_tail():
    # add a new square just behind the last one
    snake_dir.append(snake_dir[-1])
    tail = snake_pos[-1]
    dx, dy = dico[snake_dir[-1]]
    snake_pos.append(pg.Vector2(tail.x-UNIT*dx, tail.y-UNIT*dy))

def pause_screen():
    # create a new surface 
    pause_surface = pg.Surface((WIDTH*UNIT, HEIGHT*UNIT), pg.SRCALPHA)
    pg.draw.rect(pause_surface, (0, 0, 0, 20), [0, 0, WIDTH*UNIT, HEIGHT*UNIT])
    pg.draw.rect(pause_surface, (30, 30, 40), [UNIT*4, UNIT*2, UNIT*(WIDTH-8), UNIT*(HEIGHT-4)])
    en_pause = True
    while en_pause:
        mouse = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if UNIT*14 <= mouse[0] <= UNIT*18 and UNIT*7 <= mouse[1]<= UNIT*11:
                    en_pause = False
        
        # draw the play button
        if UNIT*14 <= mouse[0] <= UNIT*18 and UNIT*7 <= mouse[1]<= UNIT*11: # focused
            pg.draw.rect(pause_surface, (245, 245, 255), [UNIT*14, UNIT*7, UNIT*4, UNIT*4])
        else:
            pg.draw.rect(pause_surface, (180, 180, 190), [UNIT*14, UNIT*7, UNIT*4, UNIT*4])
        pg.draw.polygon(pause_surface, (30, 30, 40), [(UNIT*15, UNIT*8), (UNIT*17, UNIT*9), (UNIT*15, UNIT*10)])

        
        draw_screen()
        screen.blit(pause_surface, (0, 0))
        pg.display.flip()

        clock.tick(60)




def draw_screen():
    screen.fill((20, 20, 30))

    # like a checkerboard
    for i_lig in range(HEIGHT):
        for i_col in range(WIDTH):
            if (i_lig+i_col)%2 == 0:
                pg.draw.rect(screen, (24, 24, 34), pg.Rect(i_col*UNIT, i_lig*UNIT, UNIT, UNIT))

    # draw snake
    for player_pos in snake_pos:
        pg.draw.rect(screen, "white", pg.Rect(player_pos, (UNIT, UNIT)))
    # draw the eye
    dx, dy = dico[snake_dir[0]]
    x = snake_pos[0].x + UNIT//4 + UNIT//8*dx + abs(UNIT//8*dx)
    y = snake_pos[0].y + UNIT//4 + UNIT//8*dy + abs(UNIT//8*dy)
    if alive:
        pg.draw.rect(screen, (20, 20, 30), pg.Rect(x, y, UNIT//4, UNIT//4))
    else:
        pg.draw.rect(screen, (20, 20, 30), pg.Rect(x, y, UNIT//4, UNIT//10))


    # draw apple
    pg.draw.rect(screen, (230, 50, 50), pg.Rect(apple_pos[0]*UNIT, apple_pos[1]*UNIT, UNIT, UNIT))

def death_animation():
    mouvs = [1, -0.5, -0.5, -1, -1, -1, -0.5, -0.5, 1, 1, 1, 1]
    dx, dy = dico[snake_dir[0]]
    pos = snake_pos[0]
    for mouv in mouvs:
        pos.x += dx*mouv*5
        pos.y += dy*mouv*5
        draw_screen()
        pg.display.flip()
        clock.tick(60)
    
def movement(player_pos: pg.Vector2, vector: tuple[int, int]):
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


def change_direction(direction: str):
    # each square get the next direction
    for i in range(1, len(snake_dir)):
        snake_dir[len_snake-i] = snake_dir[len_snake-i-1]
    snake_dir[0] = direction


def detect_collision() -> bool:
    # move the head
    head_pos[0] = (head_pos[0] + dico[direction][0])%WIDTH
    head_pos[1] = (head_pos[1] + dico[direction][1])%HEIGHT

    # collision
    if grid[head_pos[1]][head_pos[0]] == "S":
        death_animation()
        return False
    
    grid[head_pos[1]][head_pos[0]] = "S"
    return True

def detect_apple() -> int:
    if head_pos == apple_pos: # apple eaten
        apple_pos = new_apple(grid)
        new_tail()
        return 1
    
    # remove the tail on the grid
    grid[tail_pos[1]][tail_pos[0]] = " "
    tail_pos[0] = (tail_pos[0] + dico[snake_dir[-1]][0])%WIDTH
    tail_pos[1] = (tail_pos[1] + dico[snake_dir[-1]][1])%HEIGHT
    return 0


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    if not alive:
        clock.tick(60)
        continue
    
    draw_screen()

    # get key pressed
    temp_direction = get_direction(temp_direction)

    # change direction and detect collision
    if count%(60//SPEED) == 0:
        direction = temp_direction
        change_direction(direction)
        alive = detect_collision()
        len_snake += detect_apple()

    # animate each square
    for i in range(len(snake_pos)):
        dx, dy = dico[snake_dir[i]]
        player_pos = snake_pos[i]
        movement(player_pos, (dx, dy))

    pg.display.flip()
    # limits FPS to 60
    clock.tick(60)
    count += 1

pg.quit()
