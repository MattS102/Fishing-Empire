import pygame
from classes import Player, Fish

WIDTH, HEIGHT = 1280, 720
FPS = 30

WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fish Game")
clock = pygame.time.Clock()


sprites = pygame.sprite.Group()
player = Player()
sprites.add(player)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sprites.update()

    screen.fill(WHITE)
    sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
