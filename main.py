import sys
import pickle
import pygame
import random
import os
from datetime import datetime
from suntime import Sun


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

#colors:
BLACK = (0, 0, 0)
LIGHT_GREEN = (190, 255, 170)
GREEN = (75, 225, 127)
DARK_GREEN = (55, 215, 107)
LIGHT_GREY = (210, 210, 210)
GREY = (150, 150, 150)
DARK_GREY = (130, 130, 130)
LIGHT_GOLD = (250, 240, 190)
GOLD = (235, 194, 60)
BUG_COLORS = ((242,242,114), (242, 197, 114), (242,150,114),
              (242, 145, 166), (234, 145, 242), (182, 145, 242),
              (145, 170, 242), (124,214, 235))

bg_col = LIGHT_GREEN
snake_col = GREEN
head_col = DARK_GREEN

#SETTINGS
borders_on = False
number_of_insects = 3
number_of_tiles = 20
tile_size = SCREEN_WIDTH // number_of_tiles
night_mode = 0
is_day = True
sth_changed = False





screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Simple Snake")

clock = pygame.time.Clock()
NORMAL = 10
SPEEDUP = 35
fps = NORMAL

class Snake():
    def __init__(self,x,y,orientation,color):
        self.headx = x
        self.heady = y
        self.orientation = orientation
        self.size = 3
        self.score = 0
        self.moved = True
        self.ate = False
        self.dead = False
        self.color = color
        self.segments = []
        self.segments.append(Segment(self.headx,self.heady,self.color))
        self.segments.append(Segment(self.headx - tile_size * self.orientation[0], self.heady - tile_size * self.orientation[1], self.color))
        self.segments.append(Segment(self.headx - 2 * tile_size * self.orientation[0], self.heady - 2 * tile_size * self.orientation[1], self.color))


    def eat(self):
        self.score += 10
        self.ate = True

    def draw(self):
        self.segments[0].draw(head=True)
        for s in self.segments[1:]:
            s.draw()


    def move(self):
        if self.dead:
            return


        new_one = Segment(self.headx + self.orientation[0] * tile_size, self.heady + self.orientation[1] * tile_size, self.color)
        self.segments = [new_one] + self.segments


        if self.segments[0].x < 0:
            if borders_on:
                self.die()
            else:
                self.segments[0].x = SCREEN_WIDTH - tile_size
        if self.segments[0].y < 0:
            if borders_on:
                self.die()
            else:
                self.segments[0].y = SCREEN_HEIGHT - tile_size
        if self.segments[0].x >= SCREEN_WIDTH:
            if borders_on:
                self.die()
            else:
                self.segments[0].x = 0
        if self.segments[0].y >= SCREEN_HEIGHT :
            if borders_on:
                self.die()
            else:
                self.segments[0].y = 0

        if self.ate:
            self.ate = False
        else:
            if not self.dead:
                self.segments.pop(-1)
            else:
                self.segments.pop(0)

        self.headx = self.segments[0].x
        self.heady = self.segments[0].y

        self.moved = True

    def die(self):
        player.dead = True
        global highscore, bg_col, head_col
        for ss in player.segments:
            ss.color = GREY
        bg_col = LIGHT_GREY
        head_col = DARK_GREY
        for i in insects:
            i.color = GREY
        update_high_score()

class AutoSnake(Snake):

    def __init__(self, x, y, orientation, color):
        super().__init__(x, y, orientation, color)
        self.chosen_index = 0

    def auto_turn(self):
        if self.ate:
            return
        turned = False
        insect = insects[self.chosen_index]
        if insect.x == self.headx and self.orientation[1] == 0:
            turned = True
            ry = abs(insect.y - self.heady)
            if ry < SCREEN_HEIGHT - ry:
                if insect.y < self.heady:
                    self.orientation = [0,-1]
                else:
                    self.orientation = [0, 1]
            else:
                if insect.y < self.heady:
                    self.orientation = [0, 1]
                else:
                    self.orientation = [0, -1]

        elif insect.y == self.heady and self.orientation[0] == 0:
            turned = True
            rx = abs(insect.x - self.headx)
            if rx < SCREEN_WIDTH - rx:
                if insect.x < self.headx:
                    self.orientation = [-1, 0]
                else:
                    self.orientation = [1, 0]
            else:
                if insect.x < self.headx:
                    self.orientation = [1, 0]
                else:
                    self.orientation = [-1, 0]

        next_x = self.headx + self.orientation[0] * tile_size
        next_y = self.heady + self.orientation[1] * tile_size

        for s in self.segments:
            if next_x == s.x and next_y == s.y:
                if turned:
                    self.orientation = [-x for x in self.orientation]
                else:
                    if self.orientation[0] == 0:
                        self.orientation = random.choice(([1,0],[-1,0]))

                    else:
                        self.orientation = random.choice(([0, -1], [0, 1]))

    def auto_turn2(self):
        if len(self.segments) < SCREEN_HEIGHT // tile_size:
            if self.heady == 0:
                self.orientation = [1,0]
                self.move()
                self.orientation = [0,-1]
        else:
            next_y = self.heady - tile_size
            if next_y < 0:
                next_y = SCREEN_HEIGHT - tile_size
            for s in self.segments:
                if self.headx == s.x and next_y == s.y:
                    self.orientation = [1, 0]
                    self.move()
                    self.orientation = [0, -1]
                    return

    def auto_turn3(self):
        if self.heady == 0:
            self.orientation = (1, 0)
            self.move()
            eaten = None
            for num, i in enumerate(insects):
                i.draw()
                if player.headx == i.x and player.heady == i.y:
                    player.eat()
                    eaten = num
            if eaten is not None:
                insects.pop(eaten)
                if player.score < (SCREEN_WIDTH // tile_size) * (
                        SCREEN_HEIGHT // tile_size) * 10 - 10 * number_of_insects:
                    add_insect()
            self.orientation = (0, 1)
        elif self.heady >= SCREEN_HEIGHT- tile_size :
            self.orientation = (1, 0)
            self.move()
            eaten = None
            for num, i in enumerate(insects):
                i.draw()
                if player.headx == i.x and player.heady == i.y:
                    player.eat()
                    eaten = num
            if eaten is not None:
                insects.pop(eaten)
                if player.score < (SCREEN_WIDTH // tile_size) * (
                        SCREEN_HEIGHT // tile_size) * 10 - 10 * number_of_insects:
                    add_insect()
            self.orientation = (0, -1)

class Segment():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, head=False):

        rect = pygame.rect.Rect(self.x, self.y, tile_size, tile_size)
        if is_day:
            pygame.draw.rect(screen, self.color if not head else head_col , rect)
            pygame.draw.rect(screen, bg_col, rect, 3)
        else:
            pygame.draw.rect(screen, self.color if not head else head_col, rect, 3 if not head else 5)

    def __repr__(self):
        return f"S({self.x},{self.y})"


def draw_bg(lines = False):
    if is_day:
        screen.fill(bg_col)
    else:
        screen.fill(BLACK)



def draw_scores():
    color = "black" if is_day else "white"
    font = pygame.font.SysFont("Comic Sans", 20)
    rend = font.render("Score: "+str(player.score), True, color)
    screen.blit(rend, (10, 10))
    if get_high_score() > player.score:
        rend = font.render("High Score: " + str(get_high_score()), True, color)
        screen.blit(rend, (10, 40))

def draw_borders(w=5):
    for b in borders:
        if is_day:
            pygame.draw.line(screen, BLACK, b[0], b[1], w)
        else:
            pygame.draw.line(screen, "white", b[0], b[1], w)


def write(text, y, size=20, to_right=0):
    color = "black" if is_day else "white"
    font = pygame.font.SysFont("Comic Sans", size)
    rend = font.render(text, True, color)
    screen.blit(rend, (SCREEN_WIDTH // 2 - rend.get_width() // 2 + to_right, y))

def write_long(longtext, y, letters_in_line = 50, interline = 5 ,size=20,to_right = 0):
    line = ""
    temp = 0
    for word in longtext.split():
        if len(line) + len(word) < letters_in_line:
            line = line + " " + word
        else:
            write(line, y + temp, size, to_right)
            line = word
            temp += size + interline
    write(line, y + temp, size, to_right)

def add_insect():
    possible_places = []
    for x in range(0, SCREEN_WIDTH // tile_size):
        for y in range(0,SCREEN_HEIGHT // tile_size):
            possible_places.append((x*tile_size,y*tile_size))
    for s in player.segments:
        if (s.x, s.y) in possible_places:
            possible_places.remove((s.x, s.y))
    for i in insects:
        if (i.x, i.y) in possible_places:
            possible_places.remove((i.x, i.y))
    if len(possible_places) == 0:
        return
    rx, ry = random.choice(possible_places)
    rcol = random.choice(BUG_COLORS)
    insects.append(Segment(rx, ry, rcol))

def start_screen():
    run = True
    chosen = 0
    while run:
        screen.fill(LIGHT_GREEN if is_day else BLACK)
        font = pygame.font.SysFont("Comic Sans", 80)
        rend = font.render("Simple Snake", True, GREEN)
        screen.blit(rend, (SCREEN_WIDTH // 2 - rend.get_width() // 2, SCREEN_HEIGHT / 3))

        texts = ["1. New Game", "2. Instruction", "3. Settings", "x. Exit"]
        for n, t in enumerate(texts):
            if n == chosen:
                t = ">> " + t + " <<"
            write(t, SCREEN_HEIGHT * 3/5 + n*30, 25)


        font = pygame.font.SysFont("Comic Sans", 20)
        rend = font.render("by Alex Michalec", True, GREEN)
        screen.blit(rend, (SCREEN_WIDTH - rend.get_width() -20, SCREEN_HEIGHT - rend.get_height() - 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_1:
                    return True
                if event.key == pygame.K_2:
                    instruction_screen()
                if event.key == pygame.K_3:
                    settings_screen()
                if event.key == pygame.K_x:
                    return False
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    chosen = (chosen+ 1 ) % 4
                if event.key in (pygame.K_UP, pygame.K_w):
                    chosen = (chosen - 1) % 4
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if chosen == 0:
                        return True
                    elif chosen == 1:
                        instruction_screen()
                    elif chosen == 2:
                        settings_screen()
                    elif chosen == 3:
                        return False



        pygame.display.update()

def instruction_screen():
    text = "Guide the snake to eat the food, growing longer with each meal. Avoid collisions with the walls and \
    the snake's own body. You can use WASD or the Arrow Keys to control the snake's direction. Press [Space] to \
    increase the speed of the game, but be careful! The faster speed can make controlling the snake more challenging. \
    Plan your moves ahead to avoid getting trapped. You can change the size of the board and turn on/off the walls in SETTINGS. \
    Challenge yourself to beat your high score in each game. Have Fun and Happy Snaking! "
    while True:
        screen.fill(bg_col if is_day else BLACK)

        write("Instruction:", SCREEN_HEIGHT *1/5, 30)
        write_long(text, SCREEN_HEIGHT *2/5 - 60)
        write("Press any key to comeback to the MENU!", SCREEN_HEIGHT * 4 / 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return
        pygame.display.update()

def settings_screen():
    texts = [["Size:", "Small 10x10", "Medium 20x20", "Large 40x40"],
             ["Walls:", "Off", "On"],
             ["Night mode:", "Off", "On", "Auto"],
             ["Reset the High Scores"]]
    settings = [[0,0,0],[0,0],[0,0,0]]
    chosen = [0,0]
    global number_of_insects, number_of_tiles, tile_size, sth_changed, night_mode, borders_on, is_day

    while True:
        settings[0] = [1, 0, 0] if number_of_tiles == 10 else ([0, 1, 0] if number_of_tiles == 20 else [0, 0, 1])
        settings[1] = [0, 1] if borders_on else [1, 0]
        settings[2] = [0,0,0]
        settings[2][night_mode] = 1

        screen.fill(bg_col if is_day else BLACK)

        write("Settings:", SCREEN_HEIGHT *1/5, 30)

        for sett, text in enumerate(texts):
            for option, t in enumerate(text):
                if option > 0:
                    if settings[sett][option-1]:
                        t = "[x]" + t
                    else:
                        t = "[ ]" + t
                if chosen[0] == sett and chosen[1] == option:
                    t = ">>" + t + "<<"
                if sett == 3:
                    write(t, SCREEN_HEIGHT * 3 / 5)
                else:
                    write(t, SCREEN_HEIGHT * 2/5 + option*25 - 30, to_right=200*sett - 200)


        write("Press [SPACE] to comeback to the MENU!", SCREEN_HEIGHT * 4 / 5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    save_settings()
                    return
                if event.key == pygame.K_ESCAPE:
                    save_settings()
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    chosen[0] = (chosen [0]-1) % 4
                    chosen[1] = 0
                if event.key in (pygame.K_d, pygame.K_RIGHT):
                    chosen[0] = (chosen [0]+1) % 4
                    chosen[1] = 0
                if event.key in (pygame.K_w, pygame.K_UP):
                    chosen[1] = (chosen [1]-1) % len(texts[chosen[0]])
                if event.key in (pygame.K_s, pygame.K_DOWN):
                    chosen[1] = (chosen [1]+1) % len(texts[chosen[0]])
                if event.key == pygame.K_RETURN:
                    if chosen ==[0,1]:
                        number_of_tiles = 10
                        tile_size = SCREEN_WIDTH // number_of_tiles
                        number_of_insects = 2
                        sth_changed = True
                    if chosen ==[0,2]:
                        number_of_tiles = 20
                        tile_size = SCREEN_WIDTH // number_of_tiles
                        number_of_insects = 3
                        sth_changed = True
                    if chosen ==[0,3]:
                        number_of_tiles = 40
                        tile_size = SCREEN_WIDTH // number_of_tiles
                        number_of_insects = 5
                        sth_changed = True
                    if chosen == [1,1]: #BORDERS OFF
                        borders_on = False
                        sth_changed = True
                    if chosen == [1,2]: #borders on
                        borders_on = True
                        sth_changed = True
                    if chosen == [2,1]:
                        night_mode = 0
                        is_day = True
                    if chosen == [2,2]:
                        night_mode = 1
                        is_day = False
                    if chosen == [2,3]:
                        night_mode = 2
                        is_day = is_it_day()
                    if chosen == [3,0]:
                        reset_high_scores()
                        texts[3][0] = "Scoreboard restarted succesfully."


        pygame.display.update()

def get_high_score():
    return highscores[0 if number_of_tiles == 10 else (1 if number_of_tiles == 20 else 2)][1 if borders_on else 0]

def update_high_score():
    global highscores
    if player.score > get_high_score():
        highscores[0 if number_of_tiles == 10 else (1 if number_of_tiles == 20 else 2)][1 if borders_on else 0] = player.score
        with open("scoreboard", "wb") as my_file:
            pickle.dump(highscores, my_file)

def reset_high_scores():
    global highscores
    highscores = [[0,0],[0,0],[0,0]]
    with open("scoreboard", "wb") as my_file:
        pickle.dump(highscores, my_file)

def load_settings():

    if os.path.exists("settings"):
        global tile_size, number_of_tiles, borders_on, night_mode, number_of_insects, is_day
        with open("settings", "rb") as my_file:
            temp = pickle.load(my_file)
            print(temp)
            if temp[0] in (10,20,40):
                number_of_tiles = temp[0]
                tile_size = SCREEN_WIDTH//number_of_tiles
                number_of_insects = 2 if number_of_tiles == 10 else (3 if number_of_tiles==20 else 5)
            if temp[1] in (True, False):
                borders_on = temp[1]
            if temp[2] in (0,1,2):
                night_mode = temp[2]
                if night_mode == 2:
                    is_day = is_it_day()
                else:
                    is_day = bool(not night_mode)

def save_settings():
    with open("settings", "wb") as my_file:
        pickle.dump([number_of_tiles,borders_on,night_mode],my_file)

def is_it_day():
    s = Sun(52.21, 21.00)
    sunrise = s.get_local_sunrise_time()
    sunset = s.get_sunset_time()
    now = datetime.now(tz=sunrise.tzinfo)
    return sunrise < now < sunset

highscores = [[0,0],[0,0],[0,0]]
if os.path.exists("scoreboard"):
    with open("scoreboard", "rb") as my_file:
        highscores = pickle.load(my_file)

load_settings()
run = start_screen()

player = AutoSnake(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,(0,-1),GREEN)
insects = []
for i in range(number_of_insects):
    add_insect()

#define borders
temp = 5
borders = [((temp, temp), (temp, SCREEN_HEIGHT - temp)),
           ((temp, temp), (SCREEN_WIDTH - temp, temp)),
           ((SCREEN_WIDTH - temp, SCREEN_HEIGHT - temp), (temp, SCREEN_HEIGHT - temp)),
           ((SCREEN_WIDTH - temp, SCREEN_HEIGHT - temp), (SCREEN_WIDTH - temp, temp))]
sth_changed = False


while run:
    clock.tick(fps)

    draw_bg()
    if not sth_changed:
        eaten = None
        for num, i in enumerate(insects):
            i.draw()
            if player.headx == i.x and player.heady == i.y:
                player.eat()
                eaten = num
        if eaten is not None:
            insects.pop(eaten)
            if player.score < (SCREEN_WIDTH // tile_size) * (SCREEN_HEIGHT // tile_size) * 10 - 10*number_of_insects:
                add_insect()
        player.draw()
        if borders_on:
            draw_borders()
    draw_scores()
    if player.dead:
        write("Press [SPACE] to start again", y= 380, size = 25)
        write("Press [CTRL] to go to the SETTINGS", y =420, size = 25)
        write("Press [ESC] to close the game", y = 460, size=25)


    # If WIN
    if player.score >= (SCREEN_WIDTH // tile_size) * (SCREEN_HEIGHT // tile_size) * 10 - 20:
        player.dead = True
        write("Congratulation, you won! :D", y=200, size=50)
        for s in player.segments:
            s.color = GOLD
        for i in insects:
            i.color = GOLD
        bg_col = LIGHT_GOLD
        head_col = GOLD
        update_high_score()


    # If collision with itself / DEAD
    for s in player.segments[1:]:
        if s.x == player.headx and s.y == player.heady:
            player.die()


    #player.auto_turn3()

    player.move()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            update_high_score()
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_a, pygame.K_LEFT) and player.orientation[0] == 0 and player.moved:
                player.orientation = (-1,0)
                player.moved = False
            if event.key in (pygame.K_d, pygame.K_RIGHT) and player.orientation[0] == 0 and player.moved:
                player.orientation = (1,0)
                player.moved = False
            if event.key in (pygame.K_w, pygame.K_UP) and player.orientation[1] == 0 and player.moved:
                player.orientation = (0,-1)
                player.moved = False
            if event.key in (pygame.K_s, pygame.K_DOWN) and player.orientation[1] == 0 and player.moved:
                player.orientation = (0,1)
                player.moved = False
            if event.key == pygame.K_ESCAPE:
                if player.dead:
                    run = False
                else:
                    player.die()
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL) and player.dead:
                settings_screen()
                player.score = 0
            if event.key == pygame.K_SPACE:
                if player.dead:
                    sth_changed = False
                    player = AutoSnake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, (0, -1), GREEN)
                    bg_col = LIGHT_GREEN
                    head_col = DARK_GREEN
                    insects = []
                    if night_mode == 2:
                        is_day=is_it_day()
                    for i in range(number_of_insects):
                        add_insect()
                else:
                    fps = SPEEDUP
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                fps = NORMAL


    pygame.display.update()


pygame.quit()