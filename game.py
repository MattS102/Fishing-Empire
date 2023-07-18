import pygame
import sympy
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

SEA_LEVEL = HEIGHT * 0.80

BOARDWALK_HEIGHT = HEIGHT * 0.50


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fish Game")
clock = pygame.time.Clock() 

next_background_event = pygame.USEREVENT + 1
pygame.time.set_timer(next_background_event, 2000)

background1 = pygame.image.load("images/scene/dock1.png")
background2 = pygame.image.load("images/scene/dock2.png")
proportional_background = pygame.image.load("images/scene/2dock.png")

BACKGROUNDS = [background1, background2]
background_index = 0
screen.blit(pygame.transform.scale(proportional_background, (WIDTH, HEIGHT)), (0, 0))

sprites = pygame.sprite.Group()
# -  Add new sprites here -
player = Player(125, BOARDWALK_HEIGHT)
meter = Meter(METER_CENTER[0], HEIGHT - Meter.METER_SIZE[1] - 15)
meter_active = False

sprites.add(player, player.bobber)





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
            player.cast_rod((meter.percentage/100*(WIDTH-150)+150, SEA_LEVEL))
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
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            # Print where the mouse is clicked (for testing purposes)

            pos = pygame.mouse.get_pos()
            print(pos)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player.shop_opened = not player.shop_opened
        
        # if event.type == next_background_event:
            # screen.blit(pygame.transform.scale(BACKGROUNDS[background_index%2], (WIDTH, HEIGHT)), (0, 0))
            # background_index += 1
    

    sprites.update()

    screen.blit(pygame.transform.scale(proportional_background, (WIDTH, HEIGHT)), (0, 0))

    poll_meter()

    if player.shop_opened:
        player.open_shop(screen)
    else:
        player.close_shop()

    sprites.draw(screen)


    pygame.display.flip()

pygame.quit()
