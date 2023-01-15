import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, player_sp)
        self.image = load_image('sage-frame-0.png')
        self.rect = self.image.get_rect()

        self.rect.x = 10
        self.rect.y = 200

        self.player_has_jumped = False
        if self.rect.y + self.rect.height >= 400:
            self.player_on_the_ground = True
        else:
            self.player_on_the_ground = False
        self.falling_speed = 0

        self.dx = 0

    def update(self):
        if not self.player_on_the_ground:
            self.rect.y += self.falling_speed
            self.falling_speed += 0.2
            if self.rect.y + self.rect.height >= 400:
                self.falling_speed = 0
                self.player_has_jumped = False
                self.player_on_the_ground = True

        if pygame.sprite.spritecollideany(self, enemies_sp):
            for enm in enemies_sp:
                if self.rect.y < enm.rect.y:
                    enm.death()
                    self.falling_speed = -4
                else:
                    self.death()


    def death(self):
        self.kill()

    def move(self, dx):
        self.rect.x += dx

    def jump(self):
        if self.player_on_the_ground:
            self.falling_speed = -7
            self.player_has_jumped = True
            self.player_on_the_ground = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, enemies_sp)
        self.image = load_image('enemy-frame-0.png')
        self.rect = self.image.get_rect()

        self.rect.x = 300
        self.rect.y = 200

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


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT = 500, 500
    screen = pygame.display.set_mode(size)

    '''pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))'''
    pygame.event.pump()

    FPS = 60

    all_sprites = pygame.sprite.Group()
    player_sp = pygame.sprite.Group()
    enemies_sp = pygame.sprite.Group()

    running = True
    clock = pygame.time.Clock()

    player = Player()
    enemy = Enemy()

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if any(keys):
            if keys[pygame.K_SPACE]:
                player.jump()

            if keys[pygame.K_a]:
                player.move(-3)

            if keys[pygame.K_d]:
                player.move(3)


        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
        clock.tick(FPS)


    pygame.quit()
