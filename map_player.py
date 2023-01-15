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

        self.rect.x = 300
        self.rect.y = 200

        self.player_has_jumped = False
        if self.rect.y + self.rect.height >= 400:
            self.player_on_the_ground = True
        else:
            self.player_on_the_ground = False
        self.falling_speed = 0

        self.dx = 0
        self.frame = 0

    def update(self):
        self.image = self.images[self.frame]
        if not self.player_on_the_ground:
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

        if pygame.sprite.spritecollideany(self, objects_ps):
            for obj in pygame.sprite.spritecollide(self, objects_ps, dokill=False):
                if self.rect.bottom <= obj.rect.top + 9:
                    self.player_on_the_ground = True
                    self.player_has_jumped = False
                    self.falling_speed = 0

        if pygame.sprite.spritecollideany(self, enemies_sp):
            for enm in pygame.sprite.spritecollide(self, enemies_sp, dokill=False):
                if self.rect.bottom <= enm.rect.top + 7:
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
        if pygame.sprite.spritecollideany(self, objects_ps):
            for sp in pygame.sprite.spritecollide(self, objects_ps, dokill=False):
                if sp.rect.top + 9 <= self.rect.bottom:
                    if self.rect.left < sp.rect.right - 3:
                        return False
        return True

    def can_make_left_move(self):
        if pygame.sprite.spritecollideany(self, objects_ps):
            for sp in pygame.sprite.spritecollide(self, objects_ps, dokill=False):
                if sp.rect.top + 9 <= self.rect.bottom:
                    if sp.rect.left + 3 < self.rect.right:
                        return False
        return True

    def jump(self):
        if self.player_on_the_ground:
            jump.play()
            self.falling_speed = -8
            self.player_has_jumped = True
            self.player_on_the_ground = False

    def death(self):
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
                        # will be done after putting all together


pause = False


def do_pause():
    global pause, clock
    global screen, running
    font = 100
    button1 = Button(
        "resume",
        (200, 100),
        font=font,
        bg="navy",
        feedback="resume",
        pos2=(300, 200))

    button2 = Button(
        "exit",
        (200, 250),
        font=font,
        bg="navy",
        feedback="exit",
        pos2=(100, 250))
    button3 = Button(
        "back to menu",
        (200, 400),
        font=font,
        bg="navy",
        feedback="back to menu",
        pos2=(100, 400))
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


class Objects(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        self.image = image
        super().__init__(all_sprites, objects_ps)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


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
                Objects(pf, x, y)

            if col == "@":
                pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                pf = image.load("objects/3.png")
                Objects(pf, x, y + 20)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0


if __name__ == '__main__':
    while True:
        pygame.init()
        pause = False
        mainloop()
        pygame.mixer.quit()
        pygame.mixer.init()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/melody_in_game.mp3'), loops=1000)
        pygame.mixer.Channel(0).set_volume(0.2)
        all_sprites = pygame.sprite.Group()
        size = WIDTH, HEIGHT = 700, 500
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        level = [
            "                                   ",
            "                                   ",
            "                                   ",
            "                                   ",
            "                                   ",
            "                                   ",
            "                                   ",
            "                                   ",
            "          *            -       -   ",
            "                                   ",
            "   +            +     @            ",
            "                                   ",
            "                                   ",
            "                                   ",
            "                                   ",
            "                                   ",
            "                                   ",
            "                                   ",
            "                                   ",
            "                                   "]

        '''pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))'''
        pygame.event.pump()

        FPS = 60

        all_sprites = pygame.sprite.Group()
        player_sp = pygame.sprite.Group()
        enemies_sp = pygame.sprite.Group()
        objects_ps = pygame.sprite.Group()

        running = True
        clock = pygame.time.Clock()

        Enemy(10, 350)
        Enemy(400, 350)
        Enemy(600, 200)
        player = Player()
        load_level(level)
        a = 0
        reverse = False
        font = 30
        button_pause = Button(
            "pause",
            (10, 10),
            font=font,
            bg="navy",
            feedback="pause",
            pos2=(100, 250))
        while running:
            was_move = False
            if a == 3:
                player.update_frame(reversed_image=reverse)
                a = 0
            screen.fill((255, 255, 255))
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
                        for sp in all_sprites:
                            sp.rect.x += 3
                        player.move(-3)
                        a += 1
                        was_move = True
                        reverse = True

                if keys[pygame.K_d]:
                    if player.can_make_right_move():
                        for sp in all_sprites:
                            sp.rect.x -= 3
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
