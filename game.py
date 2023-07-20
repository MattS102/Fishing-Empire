import pygame
import numpy
from random import randrange
from classes import Player, Fish, Meter, Button
import os
import time
from random import randint

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

SEA_LEVEL = HEIGHT * 0.75

BOARDWALK_HEIGHT = HEIGHT * 0.50
dblue = (0,0,139)

Cod = pygame.image.load('src/img/cod.png')
mb = pygame.image.load('src/img/_MB_.png')
Bass = pygame.image.load('src/img/bass.png')
Salmon =  pygame.image.load('src/img/salmon.png')
Trout =  pygame.image.load('src/img/trout.png')
Tuna =  pygame.image.load('src/img/tuna.png')
Wincon =  pygame.image.load('src/img/Wincon.png')
fishimgarr = {'Cod': Cod, 'Bass': Bass, 'Salmon': Salmon, 'Trout': Trout, 'Tuna': Tuna, 'Wincon': Wincon}
aapl = pygame.image.load('src/img/aquatic_abuductor.png')
chpl =  pygame.image.load('src/img/captain_hooker.png')
sspl =  pygame.image.load('src/img/salmon_slayer.png')
ttpl =  pygame.image.load('src/img/trout_terminator.png')
aa = pygame.image.load('src/img/aquatic_abductor_item.png')
ch =  pygame.image.load('src/img/captain_hooker_item.png')
ss =  pygame.image.load('src/img/salmon_slayer_item.png')
tt =  pygame.image.load('src/img/trout_terminator_item.png')
rodarr = {"aa":aa,"ch":ch,"ss":ss,"tt":tt}
chararodarr = {"aa":aapl,"ch":chpl,"ss":sspl,"tt":ttpl}

dock =  pygame.image.load('src/img/dock.png')
menu =  pygame.image.load('src/img/menu.png')
player =  pygame.image.load('src/img/player.png')
longBut =  pygame.image.load('src/img/longbutton.png')
smallBut =  pygame.image.load('src/img/smallbutton.png')

inventorybk = pygame.image.load('src/img/InventoryBackround.png')
pygame.init()
logo = pygame.image.load('src/img/Logo.png')
pygame.display.set_icon(logo)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fish Game")
clock = pygame.time.Clock() 

next_background_event = pygame.USEREVENT + 1
pygame.time.set_timer(next_background_event, 2000)


background1 = pygame.image.load("images/scene/dock1.png")
background2 = pygame.image.load("images/scene/dock2.png")
proportional_background = pygame.image.load("images/scene/2dock.png")
proportional_background = pygame.transform.scale(proportional_background, (WIDTH, HEIGHT))

BACKGROUNDS = [background1, background2]
background_index = 0
screen.blit(proportional_background, (0, 0))

sprites = pygame.sprite.Group()
# -  Add new sprites here -
player = Player(screen, 125, BOARDWALK_HEIGHT)
meter = Meter(METER_CENTER[0], HEIGHT - Meter.METER_SIZE[1] - 15)
meter_active = False

shop_opened = False

sprites.add(player)
sprites.add(meter, meter.bar)

buttons = []

# light shade of the button 
color_light = (170,170,170) 
# dark shade of the button 
color_dark = (100,100,100) 
lgreen = (144, 238, 144)


# - - - - - - - - - - - - -


def poll_meter():       

    # function to return the percentage of the meter
    # is stopped. If the meter is not stopped, this 
    # function will return None

    keystate = pygame.key.get_pressed() 

    if keystate[pygame.K_m]:
        sprites.remove(player.bobber)
        player.bobber.is_cast = False
        meter.stopped = False

    if not meter.stopped:

        if keystate[pygame.K_SPACE]:
            sprites.add(player.bobber)
            player.cast_rod((meter.percentage/100*(WIDTH-350)+350, SEA_LEVEL))
            meter.reset()
            meter.stopped = True
            
        else:
            screen.blit(meter.image, meter.position)
            screen.blit(meter.bar.image, meter.bar.position)
            meter.update()

    return meter.percentage if meter.stopped else None


# - - - - - - - - - - - - -


def drawtext(text, size, color, x , y , font_path = 'src/img/mariofont.ttf'):
    font = pygame.font.Font(font_path ,size)
    txt = font.render(text, True, color)
    rec = txt.get_rect()
    rec.center = (x,y)
    screen.blit(txt, rec)
    
def welcome_message():

    drawtext('Welcome to FISHING EMPIRE!', 80 ,dblue, WIDTH // 2, (HEIGHT // 2) - 256, font_path='fonts/8-Bit-Madness.ttf')
    drawtext('Fishing Empire is a game all about FISH!', 20, dblue, WIDTH // 2, (HEIGHT // 2) - 128)
    drawtext('The aim of the game is to catch the rarest and most valuable fish that you can and use them to buy upgrades', 20 ,dblue, WIDTH // 2, (HEIGHT // 2) - 100, font_path='fonts/8-Bit-Madness.ttf')
    drawtext('It won\'t be easy though: each cast of your rod is followed by a tricky reaction-based challenge in order to secure the fish.', 20 ,dblue,WIDTH // 2, (HEIGHT // 2) - 72, font_path='fonts/8-Bit-Madness.ttf')
    drawtext('as you progress, the shop will offer better rods and some cool power-ups!  Good Luck!', 20 ,dblue,WIDTH // 2, (HEIGHT // 2) - 44, font_path='fonts/8-Bit-Madness.ttf')

def rng_chance(percent_chance):
    # Input: a percent change scaled by 1/100 so 5 as input translates to 0.05
    # Output: True or False at random depending on the percent change
    # Remember that this will be called every game tick so the percent_chanage is PER tick 
    # so it should be kinda low

    return randrange(0, 10000) < percent_chance


#main
screen.fill((0,0,0))
screen.blit(pygame.transform.scale(logo, (WIDTH/3, WIDTH/3)), (WIDTH/2-(WIDTH/3/2), HEIGHT/2-(HEIGHT/3)))
pygame.display.flip()
pygame.time.delay(3000)
screen.blit(pygame.transform.scale(BACKGROUNDS[background_index], (WIDTH, HEIGHT)), (0, 0))
welcome_message()
pygame.display.flip()
running = True
stmenu = True
invetory_open = False
while running:
    #start menu
    if stmenu:
        while True:
            clock.tick(FPS)
            current_time = pygame.time.get_ticks()
            for ev in pygame.event.get(): 
                
                if ev.type == pygame.QUIT: 
                    pygame.quit() 
                    
                #checks if a mouse is clicked 
                if ev.type == pygame.MOUSEBUTTONDOWN: 
                    
                    #if the mouse is clicked on the 
                    # button the game is terminated 
                    if WIDTH/2 <= mouse[0] <= WIDTH/2+140 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40: 
                        pygame.quit() 
                    if WIDTH/2-200 <= mouse[0] <= WIDTH/2 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40:
                        #flashes when clicked
                        drawtext("start",35, color_dark ,WIDTH/2-100,HEIGHT/2+20)
                        pygame.display.update()
                        pygame.time.delay(100)
                        drawtext("start",35, lgreen ,WIDTH/2-100,HEIGHT/2+20)
                        pygame.display.update()
                        pygame.time.delay(100)
                        drawtext("start",35, color_dark ,WIDTH/2-100,HEIGHT/2+20)
                        pygame.display.update()
                        pygame.time.delay(100)
                        drawtext("start",35, lgreen ,WIDTH/2-100,HEIGHT/2+20)
                        pygame.display.update()
                        pygame.time.delay(100)
                        drawtext("start",35, color_dark ,WIDTH/2-100,HEIGHT/2+20)
                        pygame.display.update()
                        pygame.time.delay(100)
                        drawtext("start",35, lgreen ,WIDTH/2-100,HEIGHT/2+20)
                        pygame.display.update()
                        pygame.time.delay(100)
                        drawtext("start",35, color_dark ,WIDTH/2-100,HEIGHT/2+20)
                        pygame.display.update()
                        pygame.time.delay(100)
                        drawtext("start",35, lgreen ,WIDTH/2-100,HEIGHT/2+20)
                        pygame.display.update()
                        pygame.time.delay(100)
                        stmenu = False


            if current_time%20 == 0:
                if background_index == 1:
                    background_index = 0
                elif background_index == 0:
                    background_index = 1
                screen.blit(pygame.transform.scale(BACKGROUNDS[background_index], (WIDTH, HEIGHT)), (0, 0))
            # stores the (x,y) coordinates into 
            # the variable as a tuple 
            mouse = pygame.mouse.get_pos() 
            welcome_message()

            # if mouse is hovered on a button it 
            # changes to lighter shade 
            if WIDTH/2 <= mouse[0] <= WIDTH/2+200 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40: 
                drawtext("quit",35, lgreen ,WIDTH/2+100,HEIGHT/2+20) 
                
            else: 
                drawtext("quit",35, color_light ,WIDTH/2+100,HEIGHT/2+20) 
                
            if WIDTH/2-200 <= mouse[0] <= WIDTH/2 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40: 
                drawtext("start",35, lgreen ,WIDTH/2-100,HEIGHT/2+20) 
                
            else: 
                drawtext("start",35, color_light ,WIDTH/2-100,HEIGHT/2+20) 
            
            #update background every 2 sec

            if not stmenu:
                screen.blit(pygame.transform.scale(proportional_background, (WIDTH, HEIGHT)), (0, 0))
                pygame.display.update()
                break

            pygame.display.update()
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                player.menu_opened = not player.menu_opened
                if not player.menu_opened:
                    buttons.remove(inventory_button)
                    buttons.remove(shop_button)
                else:
                    player.menu_opened = True
                    inventory_button = Button('Inventory', WIDTH//2, 125, 450, 50, print)
                    buttons.append(inventory_button)
                    shop_button = Button('Shop', WIDTH//2, 425, 450, 50, print)
                    buttons.append(shop_button)

            if event.key == pygame.K_SPACE:
                if player.bobber.is_cast:
                    if player.has_fish:

                        drawtext("Caught a fish!!",40, dblue ,600,250)
                        drawtext(f"{Fish(meter.precentage)}", 25, dblue, 600,350)
                        pygame.display.flip()
                        player.fish_inventory.append(Fish(meter.percentage))
                        print(player.fish_inventory[-1])
                        pygame.time.delay(2000)


                        player.has_fish = False
                    else: 
                        drawtext("- No fish caught -",25, dblue ,600,250)
                        pygame.display.flip()
                        pygame.time.delay(1000)
                
                    sprites.remove(meter, meter.bar)
                    meter.reset()
                    meter.stopped = True
                    sprites.remove(player.bobber)
                    player.bobber.is_cast = False
                    
                
                else:
                    
                    if not meter.stopped:
                        
                        sprites.add(player.bobber)
                        player.cast_rod(screen, (meter.percentage/100*(WIDTH-350)+350, SEA_LEVEL))
                        player.bobber.is_cast = True
                        meter.reset()
                        meter.stopped = True
                        sprites.remove(meter, meter.bar)
            
                    else:
                        sprites.add(meter, meter.bar)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            # Print where the mouse is clicked (for testing purposes)
            if 416 <= pos[0] <= 861 and 98 <= pos[1] <= 130:
                print("invopened")
                invetory_open = True
            print(pos)
        for button in buttons:
            if event.type == pygame.MOUSEBUTTONUP:
                if button.rect.collidepoint(pygame.mouse.get_pos()):
                    button.click_handler()
    if invetory_open:
        cnt = 0   
        screen.blit(pygame.transform.scale(inventorybk,(WIDTH,HEIGHT)),(0,0))
        for i in player.fish_inventory:
            screen.blit(pygame.transform.scale(fishimgarr[i.species],(500,500)),(randint(1, WIDTH), randint(1,HEIGHT)))
        for i in player.rod_inventory:
            screen.blit(pygame.transform.scale(rodarr[i],(100,100)),(50+175*cnt,100))
            pygame.display.update()
            cnt +=1
        while invetory_open:
            pygame.display.update()
            for ev in pygame.event.get(): 
                if ev.type == pygame.QUIT: 
                    pygame.quit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        print("esc inv")
                        invetory_open = False
                        break
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    # Print where the mouse is clicked (for testing purposes)
                    if 50 <= pos[0] <= len(player.rod_inventory)*150 and 100 <= pos[1] <= 200:
                        player.ROD = player.rod_inventory[(pos[0]//150)]
                        print(player.ROD)
                    

    if rng_chance(50) and player.bobber.is_cast and not player.has_fish:
        player.has_fish = True
        sprites.add(meter, meter.bar)
        print("- Fish on the line -")
    
    if rng_chance(50) and player.has_fish:
        player.has_fish = False
        print("- Fish was lost -")
    
    
    screen.blit(proportional_background, (0, 0))
    sprites.update()

    if player.menu_opened:
        player.open_menu(screen)
    else:
        player.close_menu()

    sprites.draw(screen)

    for button in buttons:
        button.draw(screen)
    

    pygame.display.flip()

