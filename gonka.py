
from time import sleep
from pygame import *
from random import randint, choice
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(GameSprite):
    def update(self):
        global lost
        if self.rect.y < 500:
            self.rect.y += self.speed
        else:
            lost += 1
            self.rect.y = 0
            self.rect.x = choice(lines)
        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Player(GameSprite):
    def update(self):
        keys_pr = key.get_pressed()
        if keys_pr[K_RIGHT] and self.rect.x < 280:
            self.rect.x += self.speed
        if keys_pr[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    

lost = 0

window = display.set_mode((350, 550))
display.set_caption('Гонка')
clock = time.Clock()

galaxy = transform.scale(image.load('doroga.jpg'), (350, 550))
flag = True
finish = False
lines = [20, 80, 140, 200, 260]
sprite1 = Player('car10.png', 130, 400, 50, 110, 3)
monsters = sprite.Group()
for i in range(1, 5):
    monster = Enemy('car20.png', choice(lines), -40, 50, 110, randint(1,4))
    monsters.add(monster)
font.init()
font = font.SysFont('Arial', 40)
win = font.render('YOU WIN!', True, (255, 255, 0))
lose = font.render('YOU LOSE!', True, (255, 255, 0))
bullets = sprite.Group()

while flag: 
    for i in event.get():
        if i.type == QUIT:
            flag = False
    if not finish:
        
        window.blit(galaxy, (0, 0))
        sprite1.update()
        sprite1.reset()
        monsters.draw(window)
        monsters.update()
        text2 = font.render("Cчет: " + str(lost), 1, (255, 255, 1))
        window.blit(text2, (10, 50))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            monster = Enemy('car20.png', choice(lines), -40, 90, 50, randint(1,4))
            monsters.add(monster)
        if lost >= 20:
            window.blit(win, (60, 220))
            finish = True
        if sprite.spritecollide(sprite1, monsters, False):
            window.blit(lose, (60, 220))
            finish = True
        
        display.update()
    time.delay(18)