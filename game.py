import pygame
from classes import Player, Fish, Meter

WIDTH, HEIGHT = 1280, 720
FPS = 240

WHITE = (255, 255, 255)
ImgPath = 'C:\\Users\\owenc\\Documents\\GitHub\\tufts_project\\src\\img'  # fix on ur computer or code will not wok
cod = pygame.image.load(os.path.join(ImgPath, 'cod.png'))
mb = pygame.image.load(os.path.join(ImgPath, '_MB_.png'))
bass = pygame.image.load(os.path.join(ImgPath, 'bass.png'))
salmon = pygame.image.load(os.path.join(ImgPath, 'salmon.png'))
trout = pygame.image.load(os.path.join(ImgPath, 'trout.png'))
tuna = pygame.image.load(os.path.join(ImgPath, 'tuna.png'))
wincon = pygame.image.load(os.path.join(ImgPath, 'Wincon.png'))

aa = pygame.image.load(os.path.join(ImgPath, 'aquatic_abuductor.png'))
ch = pygame.image.load(os.path.join(ImgPath, 'captain_hooker.png'))
ss = pygame.image.load(os.path.join(ImgPath, 'salmon_slayer.png'))
tt = pygame.image.load(os.path.join(ImgPath, 'trout_terminator.png'))

dock = pygame.image.load(os.path.join(ImgPath, 'dock.png'))
dock2 = pygame.image.load(os.path.join(ImgPath, '2dock.png'))
dock = pygame.transform.scale(dock, (1536, 864))
dock2 = pygame.transform.scale(dock2, (1536, 864))
menu = pygame.image.load(os.path.join(ImgPath, 'menu.png'))
player = pygame.image.load(os.path.join(ImgPath, 'player.png'))
longBut = pygame.image.load(os.path.join(ImgPath, 'longbutton.png'))
smallBut = pygame.image.load(os.path.join(ImgPath, 'smallbutton.png'))
PLAYER_CENTER = (
    WIDTH // 2 - Player.PLAYER_SIZE[0] // 2,
    HEIGHT // 2 - Player.PLAYER_SIZE[1] // 2,
)

METER_CENTER = (
    WIDTH//2 - Meter.METER_SIZE[0] // 2, 
    HEIGHT // 2 - Meter.METER_SIZE[1] // 2
)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
dblue = (0, 0, 139)
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
def drawtext(text, size, color, x , y , font = 'mariofont.ttf'):
    font = pygame.font.Font(os.path.join(ImgPath, font),size)
    txt = font.render(text, True, color)
    rec = txt.get_rect()
    rec.center = (x,y)
    screen.blit(txt, rec)

def welcome_message():
    drawtext('Welcome to FISHING EMPIRE!', 56 ,dblue, X // 2, (Y // 2) - 256)
    drawtext('Fishing Empire is a game all about FISH!', 10, dblue, X // 2, (Y // 2) - 128)
    drawtext('The aim of the game is to catch the rarest and most valuable fish that you can and use them to buy upgrades', 10 ,dblue, X // 2, (Y // 2) - 100)
    drawtext('It won\'t be easy though: each cast of your rod is followed by a tricky reaction-based challenge in order to secure the fish.', 10 ,dblue,X // 2, (Y // 2) - 76)
    drawtext('as you progress, the shop will offer better rods and some cool power-ups!  Good Luck!', 10 ,dblue,X // 2, (Y // 2) - 44)
    pygame.display.update()

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

            pygame.quit()

            quit()

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

