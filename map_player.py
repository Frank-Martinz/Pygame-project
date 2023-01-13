import pygame
import os
import sys

from pygame import *

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 32


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
            for enm in enemies_sp:
                if self.rect.bottom <= enm.rect.top + 5:
                    enm.death()
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
            self.falling_speed = -8
            self.player_has_jumped = True
            self.player_on_the_ground = False

    def death(self):
        self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, enemies_sp)
        self.image = load_image('enemy-frame-0.png')
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.move = 50
        self.step = -1

        if self.rect.y + self.rect.height >= 400:
            self.on_the_ground = True
        else:
            self.on_the_ground = False

        self.falling_speed = 0

    def update(self):
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

    def death(self):
        self.kill()


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
    pygame.init()
    all_sprites = pygame.sprite.Group()
    size = WIDTH, HEIGHT = 700, 500
    screen = pygame.display.set_mode(size)
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

    player = Player()
    enemy = Enemy(10, 350)
    load_level(level)
    a = 0
    reverse = False

    while running:
        was_move = False
        if a == 3:
            player.update_frame(reversed_image=reverse)
            a = 0
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
