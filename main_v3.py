import pygame as pg
import random as rand


class Snake:
    # GAME SETTINGS
    SPEED = 6
    UNIT = 40
    WIDTH = 32
    HEIGHT = 18
    dico = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0), "": (0, 0)}

    def __init__(self, length: int, pos: list[int]):
        self.length: int = length

        self.directions: list[str] = ['E'] * length
        self.positions: list[pg.Vector2] = [pg.Vector2((pos[0]-i)*self.UNIT, pos[1]*self.UNIT) for i in range(length)]

        self.head_pos: list[int, int] = pos
        self.tail_pos: list[int, int] = [pos[0]-length+1, pos[1]]

        self.alive = True


    def change_direction(self, direction: str) -> None:
        for i in range(self.length-1):
            self.directions[self.length-i-1] = self.directions[self.length-i-2]
        self.directions[0] = direction
    
    def move_snake(self, distance: float) -> None:
        for i in range(self.length):
            dx, dy = self.dico[self.directions[i]]
            self.positions[i] += (distance*dx, distance*dy)
    
    def new_tail(self) -> None:
        x, y = self.positions[-1]
        direction = self.directions[-1]
        dx, dy = self.dico[direction]

        self.directions.append(direction)
        self.positions.append(pg.Vector2(x-dx*self.UNIT, y-dy*self.UNIT))

        self.tail_pos = [self.tail_pos[0]-dx, self.tail_pos[1]-dy]


    def movement(self, i_snake: int):
        u = self.UNIT
        player_pos = self.positions[i_snake]
        dx, dy = self.dico[self.directions[i_snake]]
        # move the square
        player_pos.x += u/60 * dx * self.SPEED
        player_pos.y += u/60 * dy * self.SPEED

        # out of screen
        if player_pos.x >= self.WIDTH*u:
            player_pos.x = 0
        elif player_pos.x <= -u:
            player_pos.x = (self.WIDTH-1)*u
        elif player_pos.y >= self.HEIGHT*u:
            player_pos.y = 0
        elif player_pos.y <= -u:
            player_pos.y = (self.HEIGHT-1)*u


class Game:
    # GAME SETTINGS
    SPEED = 6
    UNIT = 40
    WIDTH = 32
    HEIGHT = 18
    screen_size = (WIDTH*UNIT, HEIGHT*UNIT)


    def __init__(self):
        # pygame setup
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        self.surface = pg.Surface(self.screen_size, pg.SRCALPHA)
        self.clock = pg.time.Clock()

        # movement setup
        self.direction: str = ""
        self.temp_direction: str = "E"
        self.dico = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0), "": (0, 0)}

        # create the snake and a grid
        self.grid = [[' '] * self.WIDTH for _ in range(self.HEIGHT)]
        self.grid[8][15], self.grid[8][14], self.grid[8][13] = 'S', 'S', 'S'
        
        self.snake = Snake(3, [15, 8])

        # create an apple
        self.apple = [24, 8]


    def get_direction(self) -> None:
        keys = pg.key.get_pressed()
        # pause the game
        if keys[pg.K_ESCAPE]:
            self.pause_screen()
            return
        # change direction
        if keys[pg.K_z] and self.direction != "S":
            self.temp_direction = "N"
        elif keys[pg.K_s] and self.direction != "N":
            self.temp_direction = "S"
        elif keys[pg.K_q] and self.direction != "E":
            self.temp_direction = "W"
        elif keys[pg.K_d] and self.direction != "W":
            self.temp_direction = "E"


    def new_apple(self):
        # generate a new apple position (not on the snake)
        while True:
            x = rand.randint(0, self.WIDTH-1)
            y = rand.randint(0, self.HEIGHT-1)
            if self.grid[y][x] != 'S':
                self.apple = [x, y]
                return
        


    def pause_screen(self):
        u = self.UNIT

        # create a new surface 
        pause_surface = pg.Surface((self.WIDTH*u, self.HEIGHT*u), pg.SRCALPHA)
        pg.draw.rect(pause_surface, (0, 0, 0, 20), [0, 0, self.WIDTH*u, self.HEIGHT*u])
        pg.draw.rect(pause_surface, (30, 30, 40), [4*u, 2*u, (self.WIDTH-8)*u, (self.HEIGHT-4)*u])


        en_pause = True
        while en_pause:
            mouse = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if u*14 <= mouse[0] <= u*18 and u*7 <= mouse[1]<= u*11:
                        en_pause = False
            
            # draw the play button
            triangle = [(15*u, 8*u), (17*u, 9*u), (15*u, 10*u)]
            square = [14*u, 7*u, 4*u, 4*u]
            if 14*u <= mouse[0] <= 18*u and 7*u <= mouse[1]<= 11*u: # focused (in the square)
                pg.draw.rect(pause_surface, (245, 245, 255), square)
            else:
                pg.draw.rect(pause_surface, (180, 180, 190), square)
            pg.draw.polygon(pause_surface, (30, 30, 40), triangle)

            
            self.draw_screen()
            self.screen.blit(pause_surface, (0, 0))
            pg.display.flip()

            self.clock.tick(60)




    def draw_screen(self):
        u = self.UNIT
        unit_square = (u, u)

        # draw background like a checkerboard
        self.screen.fill((20, 20, 30))

        for i_lig in range(self.HEIGHT):
            for i_col in range(self.WIDTH):
                if (i_lig+i_col)%2 == 0:
                    pg.draw.rect(self.screen, (24, 24, 34), pg.Rect((i_col*u, i_lig*u), unit_square))

        # draw snake
        for player_pos in self.snake.positions:
            pg.draw.rect(self.screen, "white", pg.Rect(player_pos, unit_square))
        # draw the eye
        dx, dy = self.dico[self.direction]
        x = self.snake.positions[0].x + u//4 + u//8*dx + abs(u//8*dx)
        y = self.snake.positions[0].y + u//4 + u//8*dy + abs(u//8*dy)
        if self.snake.alive:
            pg.draw.rect(self.screen, (20, 20, 30), pg.Rect(x, y, u//4, u//4))
        else:
            pg.draw.rect(self.screen, (20, 20, 30), pg.Rect(x, y, u//4, u//10)) # eye closed


        # draw apple
        pg.draw.rect(self.screen, (230, 50, 50), pg.Rect((self.apple[0]*u, self.apple[1]*u), unit_square))

    def death_animation(self) -> None:
        self.snake.alive = False
        mouvs = [1, -0.5, -0.5, -1, -1, -1, -0.5, -0.5, 1, 1, 1, 1]
        dx, dy = self.dico[self.direction]
        head_pos = self.snake.positions[0]
        for mouv in mouvs:
            head_pos.x += dx*mouv*5
            head_pos.y += dy*mouv*5
            self.draw_screen()
            pg.display.flip()
            self.clock.tick(60)
        


    def move_head(self):
        # move the head
        self.snake.head_pos[0] += self.dico[self.direction][0]
        self.snake.head_pos[1] += self.dico[self.direction][1]

        head_x, head_y = self.snake.head_pos
        self.detect_collision()
        if self.snake.alive:
            self.grid[head_y][head_x] = "S"

    def detect_collision(self):
        head_x, head_y = self.snake.head_pos
        # out of frame
        if head_x < 0 or head_x >= self.WIDTH or head_y < 0 or head_y >= self.HEIGHT:
            self.death_animation()
        # hits its body
        elif self.grid[head_y][head_x] == "S":
            self.snake.alive = False
            self.death_animation()


    def detect_apple(self) -> int:
        if self.snake.head_pos == self.apple: # apple eaten
            self.new_apple()
            self.snake.new_tail()
            self.snake.length += 1
        
    def move_tail(self):
        self.grid[self.snake.tail_pos[1]][self.snake.tail_pos[0]] = " "
        dx, dy = self.dico[self.snake.directions[-1]]

        self.snake.tail_pos[0] += dx
        self.snake.tail_pos[1] += dy
        return 0

    def play(self):
        count = 0
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            if not self.snake.alive:
                self.clock.tick(60)
                continue
            
            self.draw_screen()

            # get key pressed
            self.get_direction()

            # change direction and detect collision (6 times per second)
            if count%(60//self.SPEED) == 0:
                self.direction = self.temp_direction
                self.snake.change_direction(self.direction)
                self.move_head()
                self.detect_apple()
                self.move_tail()

            # animate each square
            for i in range(self.snake.length):
                self.snake.movement(i)

            pg.display.flip()
            # limits FPS to 60
            self.clock.tick(60)
            count += 1

        pg.quit()

class App:
    WIDTH = 32
    HEIGHT = 18
    UNIT = 40
    screen_size = (WIDTH*UNIT, HEIGHT*UNIT)

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(self.screen_size)
        self.clock = pg.time.Clock()
        self.main_menu()
    
    def draw_menu(self):
        u = self.UNIT
        self.screen.fill((20, 20, 30))
        
        for i_lig in range(self.HEIGHT):
            for i_col in range(self.WIDTH):
                pg.draw.rect(self.screen, (24, 24, 34), [i_col*u, i_lig*u, u, u])

        mouse = pg.mouse.get_pos()
        
        play_triangle = [(15*u, 8*u), (17*u, 9*u), (15*u, 10*u)]
        play_square = [14*u, 7*u, 4*u, 4*u]
        if 14*u <= mouse[0] <= 18*u and 7*u <= mouse[1]<= 11*u: # focused (in the square)
            pg.draw.rect(self.screen, (245, 245, 255), play_square)
        else:
            pg.draw.rect(self.screen, (180, 180, 190), play_square)
        pg.draw.polygon(self.screen, (30, 30, 40), play_triangle)
    
    def main_menu(self):
        condition = True
        compteur = 0
        while condition:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    condition = False

            self.draw_menu()
            pg.display.flip()

            compteur += 1
            self.clock.tick(60)
        pg.quit()




t = App()
