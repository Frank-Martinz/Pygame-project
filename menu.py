import pygame, pyglet, ctypes, sys
from moviepy.editor import *
import os

pygame.init()
pygame.mixer.init()
path = 'beginning.mp4'

screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Menu")
clock = pygame.time.Clock()
img = pygame.image.load('menu.jpg')
font = 60


def launch():
    global screen, run
    if not os.path.isfile('for_pause.jpeg'):
        pygame.display.update()
        clip = VideoFileClip('beginning.mp4')
        clip = clip.resize(height=600)
        clip.preview()
        screen = pygame.display.set_mode((500, 600))
        pygame.display.update()
    run = False


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
        global run
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    pygame.mixer.music.load('click.mp3')
                    pygame.mixer.music.play()
                    if self.feedback == "You clicked play":
                        pygame.display.set_caption('play')
                        launch()
                        run = False
                        # redirect somewhere...
                        pygame.display.set_caption('menu')
                    if self.feedback == "You clicked help":
                        about_or_help('help.jpeg', 'help')
                        # show information for help
                    if self.feedback == "You clicked about":
                        about_or_help('about.jpeg', 'about')
                        # show about
                    if self.feedback == "exiting":
                        sys.exit()


def about_or_help(filename, text):
    screen = pygame.display.set_mode((534, 380))
    pygame.display.set_caption(text)
    img = pygame.image.load(filename)
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.load('click.mp3')
                pygame.mixer.music.play()
                flag = False
        screen.blit(img, (0, 0))
        pygame.display.update()
    screen = pygame.display.set_mode((500, 600))


run = True


def mainloop():
    global run
    pygame.init()
    pygame.mixer.init()
    path = 'beginning.mp4'
    screen = pygame.display.set_mode((500, 600))
    pygame.display.set_caption("Menu")
    clock = pygame.time.Clock()
    img = pygame.image.load('menu.jpg')
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            button1.click(event)
            button2.click(event)
            button3.click(event)
            button4.click(event)
        screen.blit(img, (0, 0))
        button1.show()
        button2.show()
        button3.show()
        button4.show()
        clock.tick(30)
        pygame.display.update()


button1 = Button(
    "play",
    (200, 100),
    font=font,
    bg="navy",
    feedback="You clicked play",
    pos2=(100, 100))

button2 = Button(
    "help",
    (200, 200),
    font=font,
    bg="navy",
    feedback="You clicked help",
    pos2=(100, 250))
button3 = Button(
    "about",
    (200, 300),
    font=font,
    bg="navy",
    feedback="You clicked about",
    pos2=(100, 400))
button4 = Button(
    "exit",
    (200, 400),
    font=font,
    bg="navy",
    feedback="exiting",
    pos2=(100, 400))
