import pygame
from classes import Player, Fish, Meter

WIDTH, HEIGHT = 1280, 720
FPS = 60

WHITE = (255, 255, 255)
PLAYER_CENTER = (
    WIDTH // 2 - Player.PLAYER_SIZE[0] // 2,
    HEIGHT // 2 - Player.PLAYER_SIZE[1] // 2,
)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fish Game")
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()
# -  Add new sprites here -
player = Player(30, PLAYER_CENTER[1])
sprites.add(player)


# - - - - - - - - - - - - -

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
