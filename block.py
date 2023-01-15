import pygame
from pygame import *
import os
import sys

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 32


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Objects(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__(all_sprites)

        self.image = image
        self.rect = self.image.get_rect()


class Level:
    def __init__(self, level):
        self.x = self.y = 0
        for row in level:
            for col in row:
                if col == "+":
                    a = Objects(image.load("objects/1.png"))
                    a.rect.x = self.x
                    a.rect.y = self.y

                if col == "*":
                    a = Objects(image.load("objects/2.png"))
                    a.rect.x = self.x
                    a.rect.y = self.y + 8

                if col == "-":
                    a = Objects(image.load("objects/4.png"))
                    a.rect.x = self.x
                    a.rect.y = self.y

                if col == "@":
                    a = Objects(image.load("objects/3.png"))
                    a.rect.x = self.x
                    a.rect.y = self.y - 20
                self.x += PLATFORM_WIDTH
            self.y += PLATFORM_HEIGHT
            self.x = 0


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
        "          *             -       -  ",
        "                                   ",
        "     +          +    @             ",
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

    running = True
    clock = pygame.time.Clock()

    Level(level)

    while running:

        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
