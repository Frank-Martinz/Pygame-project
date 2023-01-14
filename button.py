import pygame

pygame.init()
screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()
font = 60
img = pygame.image.load('menu.jpg')


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
        # pygame.draw.rect(self.surface, self.bg, pygame.Rect(self.x, self.y, self.size[0], self.size[1]), border_radius=10)

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.x, self.y = self.x1, self.y1
                    self.change_text(self.feedback, bg="red")
                    # redirect somewhere...


def mainloop():
    while True:
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
    (200, 250),
    font=font,
    bg="navy",
    feedback="You clicked help",
    pos2=(100, 250))
button3 = Button(
    "about",
    (200, 400),
    font=font,
    bg="navy",
    feedback="You clicked about",
    pos2=(100, 400))
mainloop()
