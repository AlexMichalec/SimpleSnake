import pygame
import random
import os

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
SIZE = SCREEN_WIDTH // 20

#colors:
BLACK = (0, 0, 0)
LIGHT_GREEN = (190, 255, 170)
GREEN = (75, 225, 127)
LIGHT_GREY = (210, 210, 210)
GREY = (150, 150, 150)
LIGHT_GOLD = (250, 240, 190)
GOLD = (235, 194, 60)
BUG_COLORS = ((242,242,114), (242, 197, 114), (242,150,114),
              (242, 145, 166), (234, 145, 242), (182, 145, 242),
              (145, 170, 242), (124,214, 235))

bg_col = LIGHT_GREEN
snake_col = GREEN

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Simple Snake")

clock = pygame.time.Clock()
NORMAL = 10
SPEEDUP = 30
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
        self.segments.append(Segment(self.headx - SIZE*self.orientation[0], self.heady - SIZE*self.orientation[1], self.color))
        self.segments.append(Segment(self.headx - 2* SIZE*self.orientation[0], self.heady - 2 * SIZE*self.orientation[1], self.color))

    def eat(self):
        self.score += 10
        self.ate = True

    def draw(self):
        for s in self.segments:
            s.draw()

    def move(self):
        if self.dead:
            return

        if self.ate:
            self.ate = False
        else:
            self.segments.pop(-1)

        new_one = Segment(self.headx + self.orientation[0]*SIZE, self.heady + self.orientation[1]*SIZE, self.color)
        self.segments = [new_one] + self.segments

        if self.segments[0].x < 0:
            self.segments[0].x = SCREEN_WIDTH-SIZE
        if self.segments[0].y < 0:
            self.segments[0].y = SCREEN_HEIGHT-SIZE
        if self.segments[0].x >= SCREEN_WIDTH:
            self.segments[0].x = 0
        if self.segments[0].y >= SCREEN_HEIGHT :
            self.segments[0].y = 0

        self.headx = self.segments[0].x
        self.heady = self.segments[0].y

        self.moved = True


class Segment():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        rect = pygame.rect.Rect(self.x,self.y,SIZE,SIZE)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, bg_col, rect, 3)


def draw_bg(lines = False):
    screen.fill(bg_col)
    if lines:
        for i in range (SCREEN_WIDTH//SIZE+1):
            pygame.draw.line(screen,"black",(i*SIZE,0),(i*SIZE,SCREEN_HEIGHT),3)
        for i in range (SCREEN_HEIGHT//SIZE+1):
            pygame.draw.line(screen,"black",(0,i*SIZE),(SCREEN_WIDTH, i*SIZE),3)

def draw_scores():
    font = pygame.font.SysFont("Comic Sans", 20)
    rend = font.render("Score: "+str(player.score), True, "black")
    screen.blit(rend, (10, 10))
    if highscore > player.score:
        rend = font.render("High Score: " + str(highscore), True, "black")
        screen.blit(rend, (10, 40))

def write_press_to_restart():
    font = pygame.font.SysFont("Comic Sans", 25)
    rend = font.render("Press [SPACE] to start again!", True, "black")
    screen.blit(rend, (SCREEN_WIDTH//2 - rend.get_width()//2, SCREEN_HEIGHT*2 /3))

def write_congratulation():
    font = pygame.font.SysFont("Comic Sans", 40)
    rend = font.render("Congratulation, you won :D", True, "black")
    screen.blit(rend, (SCREEN_WIDTH // 2 - rend.get_width() // 2, SCREEN_HEIGHT / 3))

def add_insect():
    rx = random.randint(0, SCREEN_WIDTH // SIZE-1) * SIZE
    ry = random.randint(0, SCREEN_HEIGHT // SIZE-1) * SIZE
    for s in player.segments:
        if s.x == rx and s.y == ry:
            add_insect()
            return
    for i in insects:
        if i.x == rx and i.y == ry:
            add_insect()
            return
    rcol = random.choice(BUG_COLORS)
    insects.append(Segment(rx, ry, rcol))

def start_screen():
    run = True
    while run:
        screen.fill(LIGHT_GREEN)
        font = pygame.font.SysFont("Comic Sans", 80)
        rend = font.render("Simple Snake", True, GREEN)
        screen.blit(rend, (SCREEN_WIDTH // 2 - rend.get_width() // 2, SCREEN_HEIGHT / 3))

        font = pygame.font.SysFont("Comic Sans", 20)
        rend = font.render("Click [SPACE] to start :D", True, BLACK)
        screen.blit(rend, (SCREEN_WIDTH // 2 - rend.get_width() // 2, SCREEN_HEIGHT * 2 / 3))

        font = pygame.font.SysFont("Comic Sans", 20)
        rend = font.render("by Alex Michalec", True, GREEN)
        screen.blit(rend, (SCREEN_WIDTH - rend.get_width() -20, SCREEN_HEIGHT - rend.get_height() - 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE:
                    return True

        pygame.display.update()


highscore = 0
if os.path.exists("scoreboard"):
    with open("scoreboard") as my_file:
        highscore = int(my_file.read())

run = start_screen()

player = Snake(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,(0,-1),GREEN)
insects = []
for i in range(3):
    add_insect()

while run:
    clock.tick(fps)

    draw_bg()
    player.draw()
    for num, i in enumerate(insects):
        i.draw()
        if player.headx == i.x and player.heady == i.y:
            player.eat()
            add_insect()
            insects.pop(num)
    draw_scores()

    # If WIN
    if player.score >= (SCREEN_WIDTH//SIZE) * (SCREEN_HEIGHT//SIZE) * 10 - 30 :
        player.dead = True
        write_press_to_restart()
        write_congratulation()
        for s in player.segments:
            s.color = GOLD
        for i in insects:
            i.color = GOLD
        bg_col = LIGHT_GOLD
        if highscore < player.score:
            highscore = player.score
            with open("Scoreboard", "w") as my_file:
                my_file.write(str(highscore))


    # If collision with itself / DEAD
    for s in player.segments[1:]:
        if s.x == player.headx and s.y == player.heady:
            player.dead = True
            write_press_to_restart()
            for ss in player.segments:
                ss.color = GREY
            bg_col = LIGHT_GREY
            for i in insects:
                i.color = GREY
            if highscore < player.score:
                highscore = player.score
                with open("Scoreboard","w") as my_file:
                    my_file.write(str(highscore))





    player.move()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if highscore < player.score:
                highscore = player.score
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
                if highscore < player.score:
                    highscore = player.score
                run = False
            if event.key == pygame.K_SPACE:
                if player.dead:
                    if highscore < player.score:
                        highscore = player.score
                    player = Snake(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, (0, -1), GREEN)
                    bg_col = LIGHT_GREEN
                    insects = []
                    for i in range(3):
                        add_insect()
                else:
                    fps = SPEEDUP
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                fps = NORMAL

    pygame.display.update()
pygame.quit()