#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x,player_y,player_speed,size_x,size_y,is_asteroid = False):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.is_asteroid = is_asteroid
    
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        player_top = self.rect.top
        player_center_x = self.rect.centerx - 10
        bullet = Bullet("bullet.png",player_center_x,player_top,15,20,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.y = -50
            self.rect.x = randint(0,win_width)
            self.speed = randint(1,4)
            if not self.is_asteroid:
                lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y >= win_height:
            self.kill()

win_width = 700
win_height = 500

window = display.set_mode((700,500))
display.set_caption("Космический Шутер")

clock = time.Clock()

background = transform.scale(image.load("galaxy.jpg"), (win_width,win_height))

mixer.init()
'''mixer.music.load("space.ogg")
mixer.music.play()'''

bullets = sprite.Group()

score = 0
lost = 0
font.init()
font1 = font.SysFont("Arial",36)
font2 = font.SysFont("Arial",72)
font3 = font.SysFont("Arial",128)
text_score = font1.render("Счет: "+ str(score),1,(255,255,255))
text_lost = font1.render("Пропущено: "+ str(lost),1,(255,255,255))
text_lose = font2.render("YOU LOSE",1,(255,0,0))
text_win = font2.render("YOU WIN!",1,(0,255,0))

enemy = Enemy("ufo.png", 450, 0, 10, 80,50)
monsters = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", randint(0,win_width-80), 0, randint(1,4), 80,50)
    monsters.add(enemy)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy("asteroid.png", randint(0,win_width-80), 0, randint(1,4), 80,50,True)
    asteroids.add(asteroid)
player = Player("rocket.png", 450, 400, 10, 80,100)

finish = False

game = True

rel_time = False
num_fire = 0

lives = 3
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    player.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    
    if finish != True:
        window.blit(background,(0,0))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        text_lost = font1.render("Пропущено: "+ str(lost),1,(255,255,255))
        text_score = font1.render("Счет: "+ str(score),1,(255,255,255))
        window.blit(text_lost,(0,25))
        window.blit(text_score,(0,0))
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reload = font1.render("Wait,reload...",1,(150,0,0))
                window.blit(reload,(260,460))

            else:
                num_fire = 0
                rel_time = False
        sprite_list = sprite.spritecollide(player,monsters,False)
        monsters_kills = sprite.groupcollide(monsters,bullets,True,True)
        asteroids_bul = sprite.groupcollide(asteroids,bullets,False,True)
        asteroids_player = sprite.spritecollide(player,asteroids,True)
        for monster in monsters_kills:
            score += 1
            enemy = Enemy("ufo.png", randint(0,win_width-80), -50, randint(1,4), 80,50)
            monsters.add(enemy)
        for i in sprite_list:
            lives -= 1
        for asteroid in asteroids_player:
            lives -= 1
        if lost >= 10 or lives <= 0:
            finish = True
            window.blit(text_lose,(200,250))
        if score >= 10:
            finish = True
            window.blit(text_win,(200,250))
        if lives == 3:
            live_text = font3.render(str(lives),1,(0,255,0))
        elif lives == 2:
            live_text = font3.render(str(lives),1,(100,255,0))
        elif lives == 1:
            live_text = font3.render(str(lives),1,(150,0,0))
        window.blit(live_text,(650,2))

    display.update()
    clock.tick(45)
