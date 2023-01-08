import pygame
from pygame import *

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 32


class Object(sprite.Sprite):
    def __init__(self, x, y, col):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        objects = {
            "-": "objects/4.png",
            "+": "objects/1.png",
            "*": "objects/2.png",
            "@": "objects/3.png",
            "#": "objects/5.png",
            " ": 1,
                   }
        if col != " ":
            self.image = image.load(objects[col])