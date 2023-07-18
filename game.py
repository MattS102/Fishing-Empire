import pygame
import numpy
from classes import Player, Fish, Meter
import os

WIDTH, HEIGHT = 1280, 720
FPS = 240

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
dblue = (0,0,139)

cod = pygame.image.load('src/img/cod.png')

mb = pygame.image.load('src/img/_MB_.png')
bass = pygame.image.load('src/img/bass.png')
salmon =  pygame.image.load('src/img/salmon.png')
trout =  pygame.image.load('src/img/trout.png')
tuna =  pygame.image.load('src/img/tuna.png')
wincon =  pygame.image.load('src/img/Wincon.png')

aa = pygame.image.load('src/img/aquatic_abuductor.png')
ch =  pygame.image.load('src/img/captain_hooker.png')
ss =  pygame.image.load('src/img/salmon_slayer.png')
tt =  pygame.image.load('src/img/trout_terminator.png')

dock =  pygame.image.load('src/img/dock.png')
menu =  pygame.image.load('src/img/menu.png')
player =  pygame.image.load('src/img/player.png')
longBut =  pygame.image.load('src/img/longbutton.png')
smallBut =  pygame.image.load('src/img/smallbutton.png')

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

def drawtext(text, size, color, x , y , font = 'mariofont.ttf'):
    font = pygame.font.Font(os.path.join(f"src/img/{font}"),size)
    txt = font.render(text, True, color)
    rec = txt.get_rect()
    rec.center = (x,y)
    screen.blit(txt, rec)
    
def welcome_message():

    drawtext('Welcome to FISHING EMPIRE!', 56 ,dblue, WIDTH // 2, (HEIGHT // 2) - 256)
    drawtext('Fishing Empire is a game all about FISH!', 10, dblue, WIDTH // 2, (HEIGHT // 2) - 128)
    drawtext('The aim of the game is to catch the rarest and most valuable fish that you can and use them to buy upgrades', 10 ,dblue, WIDTH // 2, (HEIGHT // 2) - 100)
    drawtext('It won\'t be easy though: each cast of your rod is followed by a tricky reaction-based challenge in order to secure the fish.', 10 ,dblue,WIDTH // 2, (HEIGHT // 2) - 100)
    drawtext('It won\'t be easy though: each cast of your rod is followed by a tricky reaction-based challenge in order to secure the fish.', 10 ,dblue,WIDTH // 2, (HEIGHT // 2) - 100)



#main TODO
welcome_message()
running = True
while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            pygame.quit()

            quit()

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

