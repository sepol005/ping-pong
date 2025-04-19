from pygame import *
#from random import randint

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


Player_1 = Player(K_w, K_s,"racket.png",30,200,35,100,4)
Player_2 = Player(K_UP, K_DOWN,"racket.png",520,200,35,100,4)

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

        Player_1.update()
        Player_2.update()

    display.update()
    clock.tick(FPS)