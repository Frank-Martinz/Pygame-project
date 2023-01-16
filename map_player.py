import pygame
import os
import sys
from menu import mainloop
from pygame import *

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 32

pygame.mixer.init()
pygame.mixer.set_num_channels(5)
pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/melody_in_game.mp3'), loops=1000)
pygame.mixer.Channel(0).set_volume(0.2)

jump = pygame.mixer.Sound('sounds/jump.wav')
land = pygame.mixer.Sound('sounds/landing.wav')
rebound = pygame.mixer.Sound('sounds/rebound.wav')
finish = pygame.mixer.Sound('sounds/finish.wav')


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Player(pygame.sprite.Sprite):
    images = list()
    reversed_images = list()
    for i in range(1, 14):
        images.append(load_image(f'Player_{i}.png'))

    for i in range(1, 14):
        reversed_images.append(pygame.transform.flip(load_image(f'Player_{i}.png'), True, False))

    def __init__(self):
        super().__init__(all_sprites, player_sp)
        self.images = Player.images

        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.rect.x = 30
        self.rect.y = 200

        self.player_has_jumped = False
        if self.rect.y + self.rect.height >= 400:
            self.player_on_the_ground = True
        else:
            self.player_on_the_ground = False
        self.falling_speed = 0

        self.dx = 0
        self.frame = 0

        self.has_finished = False
        self.can_walk = True

    def update(self):
        self.image = self.images[self.frame]
        if not self.player_on_the_ground:
            if self.rect.y < 0:
                self.falling_speed = 0.2
            self.rect.y += self.falling_speed
            if self.falling_speed != 7:
                self.falling_speed += 0.2
            if self.rect.y + self.rect.height >= 400:
                land.play()
                self.falling_speed = 0
                self.player_has_jumped = False
                self.player_on_the_ground = True

        if self.rect.y + self.rect.height >= 400:
            self.player_on_the_ground = True
            self.player_has_jumped = False

        else:
            self.player_on_the_ground = False
            self.player_has_jumped = True

        if pygame.sprite.spritecollideany(self, finish_sp) and not self.has_finished:
            finish_level()
            self.has_finished = True

        if pygame.sprite.spritecollideany(self, objects_ps):
            for obj in pygame.sprite.spritecollide(self, objects_ps, dokill=False):
                if self.rect.bottom <= obj.rect.top + 9:
                    self.player_on_the_ground = True
                    self.player_has_jumped = False
                    self.falling_speed = 0
                if self.rect.top <= obj.rect.bottom and self.rect.bottom > obj.rect.bottom:
                    if obj.rect.left < self.rect.left and obj.rect.right > self.rect.right:
                        if not obj.can_walk:
                            self.falling_speed = 0.2
                            self.rect.y += 3

        if pygame.sprite.spritecollideany(self, enemies_sp):
            for enm in pygame.sprite.spritecollide(self, enemies_sp, dokill=False):
                if self.rect.bottom <= enm.rect.top + 9:
                    enm.death()
                    rebound.play()
                    self.falling_speed = -4
                else:
                    self.death()
                    return

    def update_frame(self, reversed_image=False):
        self.frame += 1
        if self.frame == 12:
            self.frame = 0

        if reversed_image:
            self.images = Player.reversed_images
        else:
            self.images = Player.images

    def move(self, dx):
        self.rect.x += dx

    def can_make_right_move(self):
        if self.has_finished is True:
            return False

        if pygame.sprite.spritecollideany(self, objects_ps):
            for sp in pygame.sprite.spritecollide(self, objects_ps, dokill=False):
                if sp.can_walk:
                    if self.rect.x >= 690:
                        return False
                    return True

                if sp.rect.top + 9 <= self.rect.bottom:
                    if self.rect.left < sp.rect.right - 3:
                        return False
        if self.rect.x >= 690:
            return False
        return True

    def can_make_left_move(self):
        if self.has_finished is True:
            return False

        if pygame.sprite.spritecollideany(self, objects_ps):
            for sp in pygame.sprite.spritecollide(self, objects_ps, dokill=False):
                if sp.can_walk:
                    if self.rect.x <= 3:
                        return False
                    return True
                if sp.rect.top + 9 <= self.rect.bottom:
                    if sp.rect.left + 3 < self.rect.right:
                        return False

        if self.rect.x <= 3:
            return False
        return True

    def jump(self):
        if self.player_on_the_ground:
            jump.play()
            self.falling_speed = -8
            self.player_has_jumped = True
            self.player_on_the_ground = False

    def death(self):
        gameover()
        pygame.mixer.music.stop()
        self.kill()


class Enemy(pygame.sprite.Sprite):
    images = list()
    for i in range(8):
        images.append(load_image(f'enemy_frames/enemy_frame_{i}.png'))

    reversed_images = list()
    for i in range(8):
        reversed_images.append(pygame.transform.flip(load_image(f'enemy_frames/enemy_frame_{i}.png'), True, False))

    death_image = load_image(f'enemy_frames/enemy_death.png')

    def __init__(self, x, y):
        super().__init__(all_sprites, enemies_sp)
        self.images = Enemy.images
        self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.move = 50
        self.step = -1

        self.alive = True

        if self.rect.y + self.rect.height >= 400:
            self.on_the_ground = True
        else:
            self.on_the_ground = False

        self.falling_speed = 0

        self.cyc = 0
        self.frame = 0

    def update(self):
        if not self.alive:
            return

        self.update_frame()

        if not self.on_the_ground:
            self.falling_speed += 0.2
            self.rect.y += self.falling_speed
            if self.rect.y + self.rect.height >= 400:
                self.falling_speed = 0
                self.on_the_ground = True

        if self.move == 50:
            self.step = -1
        elif self.move == -50:
            self.step = 1

        self.move += self.step
        self.rect.x += self.step

    def update_frame(self):
        self.cyc += 1
        if self.cyc == 3:
            self.frame += 1
            self.cyc = 0
        if self.frame == 8:
            self.frame = 0

        if self.step == -1:
            self.images = Enemy.images
            self.image = self.images[self.frame]
        else:
            self.images = Enemy.reversed_images
            self.image = self.images[self.frame]

    def death(self):
        enemies_sp.remove(self)
        self.alive = False
        if self.step == -1:
            self.image = Enemy.death_image
        else:
            self.image = pygame.transform.flip(Enemy.death_image, True, False)


class Finish(pygame.sprite.Sprite):
    image = load_image('finish.png')

    def __init__(self):
        super().__init__(all_sprites, finish_sp)
        self.image = Finish.image
        self.rect = self.image.get_rect()

        self.rect.x = 2885
        self.rect.y = 200


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, pos, font, bg="black", feedback="", pos2=(0, 0)):
        self.x, self.y = pos
        self.x1, self.y1 = pos2
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)

    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        self.bg = bg
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()[0] + 5, self.text.get_size()[1] + 5
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self):
        screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        global pause, screen, running
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    pygame.mixer.music.load('click.mp3')
                    pygame.mixer.music.play()
                    if self.feedback == 'pause':
                        do_pause()
                    if self.feedback == 'resume':
                        pause = False
                    if self.feedback == 'exit':
                        sys.exit()
                    if self.feedback == 'back to menu':
                        running = False
                    if self.feedback == 'play' or self.feedback == 'restart':
                        setup_level()
                        pause = False
                    if self.feedback == 'next level':
                        lvl = int(open('data/info.txt', 'r').readlines(1)[0].split(': ')[1])
                        lvl += 1
                        f = open('data/info.txt', 'w').write(f'level: {lvl}')
                        setup_level()
                        pause = False

                    if self.feedback == 'back to menu and level complete':
                        lvl = int(open('data/info.txt', 'r').readlines(1)[0].split(': ')[1])
                        lvl += 1
                        f = open('data/info.txt', 'w').write(f'level: {lvl}')
                        running = False
                        # will be done after putting all together


class Objects(pygame.sprite.Sprite):
    def __init__(self, image, x, y, can_walk=False):
        self.image = image
        super().__init__(all_sprites, objects_ps)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.can_walk = can_walk


pause = False


def do_pause():
    global pause, clock
    global screen, running
    font = 100
    button1 = Button(
        "resume",
        (100, 50),
        font=font,
        bg="orange",
        feedback="resume",
        pos2=(300, 150))

    button2 = Button(
        "exit",
        (100, 200),
        font=font,
        bg="orange",
        feedback="exit",
        pos2=(300, 300))
    button3 = Button(
        "back to menu",
        (100, 350),
        font=font,
        bg="orange",
        feedback="back to menu",
        pos2=(300, 450))
    pause = True
    pygame.display.set_caption("Pause")
    img = pygame.image.load('for_pause.jpeg')
    while pause and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event)
            button2.click(event)
            button3.click(event)
        screen.blit(img, (0, 0))
        button1.show()
        button2.show()
        button3.show()
        pygame.display.update()
    clock = pygame.time.Clock()


def gameover():
    global pause, clock
    global screen, running
    font = 100
    button1 = Button(
        "play",
        (45, 290),
        font=font,
        bg="orange",
        feedback="play",
        pos2=(230, 310))

    button3 = Button(
        "back to menu",
        (350, 290),
        font=font,
        bg="orange",
        feedback="back to menu",
        pos2=(650, 350))
    pause = True
    pygame.display.set_caption("gameover")
    img = pygame.image.load('data/gameover.png')
    img = pygame.transform.scale(img, (750, 600))
    while pause and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event)
            button3.click(event)
        screen.blit(img, (0, 0))
        button1.show()
        button3.show()
        screen.blit(img, (0, 0))
        pygame.display.update()
    clock = pygame.time.Clock()


def finish_level():
    pygame.mixer.Channel(0).stop()
    finish.play()

    global pause, clock
    global screen, running
    font = 100
    button1 = Button(
        "next level",
        (10, 230),
        font=font,
        bg="navy",
        feedback="next level",
        pos2=(320, 265))

    button2 = Button(
        'restart',
        (4, 320),
        font=font,
        bg="navy",
        feedback="restart",
        pos2=(305, 360)
    )

    button3 = Button(
        "back to menu",
        (6, 430),
        font=font,
        bg="navy",
        feedback="back to menu and level complete",
        pos2=(320, 470))

    pause = True
    pygame.display.set_caption("level complete!!")
    img = pygame.image.load('data/level_complete.png')
    img = pygame.transform.scale(img, (725, 600))
    while pause and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event)
            button2.click(event)
            button3.click(event)
        screen.blit(img, (0, 0))
        button1.show()
        button2.show()
        button3.show()
        screen.blit(img, (0, 0))
        pygame.display.update()
    clock = pygame.time.Clock()


def load_level(level):
    x = y = 0
    for row in level:
        for col in row:
            if col == "+":
                pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                pf = image.load("objects/1.png")
                Objects(pf, x, y + 45)

            if col == "*":
                pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                pf = image.load("objects/2.png")
                Objects(pf, x, y + 8)

            if col == "-":
                pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                pf = image.load("objects/4.png")
                Objects(pf, x, y, can_walk=True)

            if col == "@":
                pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                pf = image.load("objects/3.png")
                Objects(pf, x, y + 20)

            if col == '&':
                Enemy(x, 350)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0


def setup_level():
    global all_sprites, player_sp, enemies_sp, objects_ps
    global player, screen_x

    pygame.display.set_caption("Secret Lands")

    pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/melody_in_game.mp3'), loops=1000)
    pygame.mixer.Channel(0).set_volume(0.2)

    lvl = int(open('data/info.txt', 'r').readlines(1)[0].split(': ')[1])
    level = open(f'data/level_{lvl}.txt', 'r').read()

    all_sprites = pygame.sprite.Group()
    player_sp = pygame.sprite.Group()
    enemies_sp = pygame.sprite.Group()
    objects_ps = pygame.sprite.Group()
    finish_sp = pygame.sprite.Group()

    Finish()
    player = Player()
    load_level(level.split('\n'))

    screen_x = 0
    screen.blit(background_image, (screen_x, 0))


if __name__ == '__main__':
    while True:
        pygame.display.set_caption("Secret Lands")
        pygame.init()
        pause = False
        mainloop()
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/melody_in_game.mp3'), loops=1000)
        pygame.mixer.Channel(0).set_volume(0.2)
        background_image = pygame.image.load('data/level1.png')
        all_sprites = pygame.sprite.Group()
        size = WIDTH, HEIGHT = 700, 500
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        lvl = int(open('data/info.txt', 'r').readlines(1)[0].split(': ')[1])
        level = open(f'data/level_{lvl}.txt', 'r').read()

        pygame.event.pump()

        FPS = 60

        all_sprites = pygame.sprite.Group()
        player_sp = pygame.sprite.Group()
        enemies_sp = pygame.sprite.Group()
        objects_ps = pygame.sprite.Group()
        finish_sp = pygame.sprite.Group()

        running = True
        clock = pygame.time.Clock()

        Finish()
        player = Player()
        load_level(level.split('\n'))
        a = 0
        reverse = False
        font = 30
        button_pause = Button(
            "pause",
            (10, 10),
            font=font,
            bg="orange",
            feedback="pause",
            pos2=(100, 250))

        screen_x = 0
        while running:
            was_move = False
            if a == 3:
                player.update_frame(reversed_image=reverse)
                a = 0
            screen.fill((255, 255, 255))
            screen.blit(background_image, (screen_x, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                button_pause.click(event)

            keys = pygame.key.get_pressed()
            if any(keys):
                if keys[pygame.K_SPACE]:
                    player.jump()

                if keys[pygame.K_a]:
                    if player.can_make_left_move():
                        if screen_x <= -3 and player.rect.x == 300:
                            for sp in all_sprites:
                                sp.rect.x += 3

                            screen_x += 3
                        player.move(-3)
                        a += 1
                        was_move = True
                        reverse = True

                if keys[pygame.K_d]:
                    if player.can_make_right_move():
                        if screen_x >= -2277 and player.rect.x == 300:
                            for sp in all_sprites:
                                sp.rect.x -= 3

                            screen_x -= 3
                        player.move(3)
                        a += 1
                        was_move = True
                        reverse = False

            if not was_move:
                a = 0
                player.frame = 0

            all_sprites.update()
            all_sprites.draw(screen)
            pygame.image.save(screen, "for_pause.jpeg")
            button_pause.show()
            pygame.display.update()
            clock.tick(FPS)
