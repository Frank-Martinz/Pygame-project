import pygame
from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"
GROUND = "#783708"


def main():
    PLATFORM_WIDTH = 60
    PLATFORM_HEIGHT = 32
    PLATFORM_COLOR = "#FF6262"
    level = [
        "                                   ",
        "                                   ",
        "                                   ",
        "                                   ",
        "                                   ",
        "                                   ",
        "                                   ",
        "                                   ",
        "            *            -         ",
        "                                   ",
        "     +                @            ",
        "                                   ",
        "                                   ",
        "                                   ",
        "                                   ",
        "                                   ",
        "                                   ",
        "                                   ",
        "                                   ",
        "                                   "]
    # + - маленькая кочка, * - большая кочка, @ - камень, - платформа, # - огонь
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Secret Lands")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        screen.blit(bg, (0, 0))
        ground = Surface((WIN_WIDTH, 260))
        ground.fill(Color(GROUND))
        screen.blit(ground, (0, 400))
        x = y = 0

        for row in level:
            for col in row:
                if col == "+":

                    pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    pf = image.load("1.png")
                    screen.blit(pf, (x, y))

                if col == "*":

                    pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    pf = image.load("2.png")
                    screen.blit(pf, (x, y + 8))

                if col == "-":

                    pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    pf = image.load("4.png")
                    screen.blit(pf, (x, y))

                if col == "@":

                    pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    pf = image.load("3.png")
                    screen.blit(pf, (x, y - 20))

                x += PLATFORM_WIDTH
            y += PLATFORM_HEIGHT
            x = 0
        pygame.display.update()


if __name__ == "__main__":
    main()
