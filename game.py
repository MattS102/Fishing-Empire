import pygame
from classes import Player, Fish, Meter

WIDTH, HEIGHT = 1280, 720
FPS = 60

WHITE = (255, 255, 255)

PLAYER_CENTER = (
    WIDTH // 2 - Player.PLAYER_SIZE[0] // 2,
    HEIGHT // 2 - Player.PLAYER_SIZE[1] // 2,
)

METER_CENTER = (
    WIDTH//2 - Meter.METER_SIZE[0] // 2, 
    HEIGHT // 2 - Meter.METER_SIZE[1] // 2
)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fish Game")
clock = pygame.time.Clock()

sprites = pygame.sprite.Group()
# -  Add new sprites here -
player = Player(30, PLAYER_CENTER[1])
meter = Meter(METER_CENTER[0], HEIGHT - Meter.METER_SIZE[1] - 15)
meter_active = False
sprites.add(player)



# - - - - - - - - - - - - -


def poll_meter():       

    # function to return the percentage of the meter
    # is stopped. If the meter is not stopped, this 
    # function will return None

    keystate = pygame.key.get_pressed() 

    if keystate[pygame.K_m]:
        meter.stopped = False

    if not meter.stopped:

        if keystate[pygame.K_SPACE]:
            
            meter.reset()
            meter.stopped = True
            
            

        else:
            screen.blit(meter.image, meter.position)
            screen.blit(meter.bar.image, meter.bar.position)
            meter.update()

    return meter.percentage if meter.stopped else None

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            # Print where the mouse is clicked (for testing purposes)

            pos = pygame.mouse.get_pos()
            print(pos)
    

    sprites.update()

    screen.fill(WHITE)

    result = poll_meter()

    if result != None and meter.stopped:
        
        # get meter result here. for example:
        # score = result * 10

        result = None
        meter.reset()

    sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
