from pygame import *
#from random import randint

font.init()

WIDTH = 600
HEIGHT = 400
FPS = 60
WIN_SCORE = 10
RESTART_TIME = 1000

#BACKGROUNGD_COLOR = (randint(0,225),randint(0,225),randint(0,225))
BACKGROUNGD_COLOR = (10,10,50)
RED = (150, 0, 0)
GREEN = (0,150,0)
WHITE = (225,225,225)

score_1 = 0
score_2 = 0
font_score = font.Font(None,50)
font_text = font.Font(None,36)

lose1 = font_text.render("PLAYER 1 LOSE", True, RED)
lose2 = font_text.render("PLAYER 2 LOSE", True, RED)
win1 = font_text.render("PLAYER 1 WIN", True, GREEN)
win2 = font_text.render("PLAYER 2 WIN", True, GREEN)

window = display.set_mode((WIDTH,HEIGHT))
display.set_caption("Ping-Pong Yoy")
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))


class Player(GameSprite):
    def __init__(self, up, down, img, x, y, w, h, speed):
        super().__init__(img,x,y,w,h)
        self.speed = speed
        self.up = up
        self.down = down

    def update(self):
        keys = key.get_pressed()
        if keys[self.up] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[self.down] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, img, x, y, w, h, dx, dy):
        super().__init__(img,x,y,w,h)
        self.dx = dx
        self.dy = dy
        self.tail = []

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        self.tail.append((self.rect.centerx, self.rect.centery))
        if len(self.tail)>10:
            self.tail.pop(0)
    
    def draw_tail(self):
        for i, pos in enumerate(self.tail):
            alpha = 255 * (i / len(self.tail))
            s = Surface((10, 10), SRCALPHA)
            s.fill((255, 255, 255, int(alpha)))
            window.blit(s, (pos[0]-5,pos[1]-5))

Player_1 = Player(K_w, K_s,"racket.png",30,200,35,100,4)
Player_2 = Player(K_UP, K_DOWN,"racket.png",520,200,35,100,4)
ball = Ball("tenis_ball.png",200,200,50,50,3,3)

run = True
finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        window.fill(BACKGROUNGD_COLOR)
        Player_1.reset()
        Player_2.reset()
        ball.reset()

        Player_1.update()
        Player_2.update()
        ball.update()
        ball.draw_tail()
    
    if ball.rect.y > HEIGHT - 50 or ball.rect.y < 0:
        ball.dy *= -1
    
    if sprite.collide_rect(Player_1,ball) or sprite.collide_rect(Player_2,ball):
        ball.dx *= -1

    if ball.rect.x < 0:
        score_2 += 1
        ball.rect.x = 200
        ball.rect.y = 200


    if ball.rect.x > WIDTH:
        score_1 += 1
        ball.rect.x = 200
        ball.rect.y = 200

    score_text = str(score_1) + ":" + str(score_2)
    score_img = font_score.render(score_text, True, WHITE)
    score_rect = score_img.get_rect(center=(WIDTH//2,50))
    window.blit(score_img,score_rect)

    if score_1 >= WIN_SCORE or score_2 >= WIN_SCORE:
        finish = True
        if score_1 > score_2:
            window.blit(win1,(200,200))
            window.blit(lose2,(200,250))
        else:
            window.blit(win2,(200,200))
            window.blit(lose1,(200,250))

    display.update()
    clock.tick(FPS)