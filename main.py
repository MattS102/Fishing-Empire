import pygame
from random import randrange, randint
from classes import Player, Fish, Meter, Button, Item, ItemFrame

WIDTH, HEIGHT = 1280, 720
FPS = 40

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

print('Loading...')

pygame.init()
logo = pygame.image.load('src/img/Logo.png')
pygame.display.set_icon(logo)

# Fish Images 
cod = pygame.image.load('src/img/cod.png')
mb = pygame.image.load('src/img/_MB_.png')
bass = pygame.image.load('src/img/bass.png')
salmon =  pygame.image.load('src/img/salmon.png')
trout =  pygame.image.load('src/img/trout.png')
tuna =  pygame.image.load('src/img/tuna.png')
Wincon =  pygame.image.load('src/img/wincon.png')


# Rod Images        

Cod = pygame.image.load('src/img/cod.png')
mb = pygame.image.load('src/img/_MB_.png')
Bass = pygame.image.load('src/img/bass.png')
Salmon =  pygame.image.load('src/img/salmon.png')
Trout =  pygame.image.load('src/img/trout.png')
Tuna =  pygame.image.load('src/img/tuna.png')
Wincon =  pygame.image.load('src/img/wincon.png')
fishimgarr = {'Cod': Cod, 'Bass': Bass, 'Salmon': Salmon, 'Trout': Trout, 'Tuna': Tuna, 'Wincon': Wincon}
aapl = pygame.transform.scale(pygame.image.load('src/img/aquatic_abuductor.png'),Player.PLAYER_SIZE)
chpl =  pygame.transform.scale(pygame.image.load('src/img/captain_hooker.png'),Player.PLAYER_SIZE)
sspl =  pygame.transform.scale(pygame.image.load('src/img/salmon_slayer.png'),Player.PLAYER_SIZE)
ttpl =  pygame.transform.scale(pygame.image.load('src/img/trout_terminator.png'),Player.PLAYER_SIZE)
aa = pygame.image.load('src/img/aquatic_abductor_item.png')
ch =  pygame.image.load('src/img/captain_hooker_item.png')
ss =  pygame.image.load('src/img/salmon_slayer_item.png')
tt =  pygame.image.load('src/img/trout_terminator_item.png')
coinup = pygame.transform.scale(pygame.image.load('src/img/coin-up.png'),(128,128))
luckup =  pygame.transform.scale(pygame.image.load('src/img/PowerUp-Clover.png'),(128,128))
slowtime =  pygame.transform.scale(pygame.image.load('src/img/slow-time.png'),(128,128))
rodarr = {"aa":aa,"ch":ch,"ss":ss,"tt":tt}
chararodarr = {"aa":aapl,"ch":chpl,"ss":sspl,"tt":ttpl}
rods_convert = {"ch" : "Captain Hooker", "ss": "Salmon Slayer", "tt": "Trout Terminator", "aa": "Aquatic Abductor"}
pwruparr = {"coinup" : coinup, "luckup" : luckup, "slowtime" : slowtime}
power_up_convert = {"coinup" : "Double Coins", "luckup" : "Lucky Catch", "slowtime" : "Slower Meter"}



#Scene and Menu Images
dock =  pygame.image.load('src/img/dock.png')
menu =  pygame.image.load('src/img/menu.png')
player =  pygame.image.load('src/img/player.png')
longBut =  pygame.image.load('src/img/longbutton.png')
smallBut =  pygame.image.load('src/img/smallbutton.png')

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN )
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
long_menu_image = pygame.image.load('images/menu/menu_long.png')

inventorybk = pygame.image.load('src/img/InventoryBackround.png')

sprites = pygame.sprite.Group()
# -  Add new sprites here -
player = Player(screen, 125, BOARDWALK_HEIGHT)
meter = Meter(METER_CENTER[0], HEIGHT - Meter.METER_SIZE[1] - 15)

meter_active = False

shop_opened = False
inventory_opened = False

sprites.add(player)
sprites.add(meter, meter.bar)

position_list = []

buttons = []
item_frames = []
rods = {"Captain Hooker" : 500, "Salmon Slayer" : 1500, "Trout Terminator" : 4000, "Aquatic Abductor" : 10000}
power_ups = {"Slow-Time" : 500, "1 in a Million" : 800, "Double Down" : 1000}


# light shade of the button 
color_light = (170,170,170) 
# dark shade of the button 
color_dark = (100,100,100) 
lgreen = (144, 238, 144)


global text_list
text_list = []

for i, (rod, price) in enumerate(rods.items()):
    new_frame = ItemFrame(Item(rod.lower().replace(" ", "_"), price), i*200 + 255, 100)
    item_frames.append(new_frame)

for i, (power_up, price) in enumerate(power_ups.items()):
    new_frame = ItemFrame(Item(power_up, price), i*200 + 355, 350)
    new_frame.is_bought = True
    item_frames.append(new_frame)


def drawtext(text, size, color, x , y , duration=None, font_path = 'src/img/mariofont.ttf'):
    init_time = pygame.time.get_ticks()
    text_list.append((init_time, duration, [text, size, color, x, y, font_path]))

def static_draw_text(text, size, color, x, y, font_path = 'src/img/mariofont.ttf'):
    font = pygame.font.Font(font_path ,size)
    txt = font.render(text, True, color)
    rec = txt.get_rect()
    rec.center = (x,y)
    screen.blit(txt, rec)
    

def draw_all_text():
    _text_list = []
    global text_list

    for text_and_params in text_list:
        init_time, duration, params = text_and_params
        current_time =  pygame.time.get_ticks()

        if duration == None:

            text, size, color, x, y, font_path = params


            font = pygame.font.Font(font_path ,size)

            if isinstance(text, str):
                txt = font.render(text, True, color)
            else:
                txt = text

            rec = txt.get_rect()
            rec.center = (x,y)
            screen.blit(txt, rec)

            

            if stmenu:
                _text_list.append(text_and_params)

        elif current_time <= init_time + duration:

            text, size, color, x, y, font_path = params

            font = pygame.font.Font(font_path ,size)

            if isinstance(text, str):
                txt = font.render(text, True, color)
            else:
                txt = text
        
            rec = txt.get_rect()
            rec.center = (x,y)
            screen.blit(txt, rec)
        
            _text_list.append(text_and_params)
        
        text_list = _text_list
        
    
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
                        for i in range(8):
                            static_draw_text("start",35, lgreen if i % 2 == 0 else color_dark  ,WIDTH/2-100,HEIGHT/2+20)
                            pygame.display.update()
                            pygame.time.delay(100)

                        stmenu = False


            # if current_time%20 == 0:
                #if background_index == 1:
                    #background_index = 0
                #elif background_index == 0:
                    #background_index = 1
                #screen.blit(pygame.transform.scale(BACKGROUNDS[background_index], (WIDTH, HEIGHT)), (0, 0))
            # stores the (x,y) coordinates into 
            # the variable as a tuple 
            mouse = pygame.mouse.get_pos() 
            welcome_message()

            # if mouse is hovered on a button it 
            # changes to lighter shade 
            if WIDTH/2 <= mouse[0] <= WIDTH/2+200 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40: 
                static_draw_text("quit",35, lgreen ,WIDTH/2+100,HEIGHT/2+20) 
                
            else: 
                static_draw_text("quit",35, color_light ,WIDTH/2+100,HEIGHT/2+20) 
                
            if WIDTH/2-200 <= mouse[0] <= WIDTH/2 and HEIGHT/2 <= mouse[1] <= HEIGHT/2+40: 
                static_draw_text("start",35, lgreen ,WIDTH/2-100,HEIGHT/2+20) 
                
            else: 
                static_draw_text("start",35, color_light ,WIDTH/2-100,HEIGHT/2+20) 
            
            #update background every 2 sec
            draw_all_text()

            if not stmenu:
                screen.blit(pygame.transform.scale(proportional_background, (WIDTH, HEIGHT)), (0, 0))
                pygame.display.update()
                draw_all_text()
                break

            pygame.display.update()
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            pygame.quit()

        if event.type == pygame.MOUSEBUTTONUP:
            # Print where the mouse is clicked (for testing purposes)
            pos = pygame.mouse.get_pos()
            #print(pos)
            if inventory_opened:
                try:
                    if 900 < pos[0] < 950 and 125 < pos[1] < 225:
                        player.use_powerup(0)
                    if 1050 < pos[0] < 1200 and 125 < pos[1] < 175:
                        player.use_powerup(1)
                    if 950 < pos[0] < 1080 and 200 < pos[1] < 275:
                        player.use_powerup(2)
                except IndexError:
                    drawtext("used!", 100, dblue, WIDTH/2,HEIGHT/2)


        if "slowtime" in player.powerupstat:
            meter.bar.speed = 10
        
        else:
            meter.bar.speed = 25

        
        if True not in (shop_opened, inventory_opened):

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_e, pygame.K_ESCAPE):
                    if player.menu_opened:
            
                        buttons.remove(inventory_button)
                        buttons.remove(shop_button)
                    else:
                        inventory_button = Button('Inventory', WIDTH//2, HEIGHT//2-100, 450, 50, print)
                        buttons.append(inventory_button)

                        shop_button = Button('Shop', WIDTH//2, HEIGHT//2, 450, 50, print)
                        buttons.append(shop_button)

                    player.menu_opened = not player.menu_opened
                    
                    
            
            for button in buttons:
                if event.type == pygame.MOUSEBUTTONUP:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        if button.text == 'Inventory':
                            inventory_opened = True
                        
                        if button.text == 'Shop':
                            shop_opened = True
                            
                            
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.bobber.is_cast:

                        if player.has_fish:
                            
                            text_list = []
                            drawtext("- Caught a fish!! -",32, dblue ,610,215, duration=3000)

                            new_fish = Fish(100 if "luckup" in player.powerupstat else meter.percentage)
                            drawtext(repr(new_fish), 16, dblue ,610,250,duration=3000)

                            player.fish_inventory.append(new_fish)
                            #print(player.fish_inventory[-1])

                            payout = Fish.RARITY_DICT[new_fish.rarity] * Fish.SPECIES_DICT[new_fish.species] * (2 if "coinup" in player.powerupstat else 1)
                            drawtext(f"+{payout}", 16, pygame.Color(0, 0, 0), 40 , 40,duration=3000)

                            player.coins += payout


                            player.has_fish = False


                    
                        else: 
                            text_list = []
                            #print("- No fish caught -")
                            drawtext("- No fish caught -",32, dblue ,610,215, duration=3000)
                        

                    
                        sprites.remove(meter, meter.bar)
                        meter.reset()
                        meter.stopped = True
                        sprites.remove(player.bobber)
                        player.bobber.is_cast = False
                        
                    
                    else:
                        text_list = []
                        
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
                    #print("invopened")
                    invetory_open = True
                    #print(pos)
                
        elif shop_opened:
            for frame in item_frames:
                if event.type == pygame.MOUSEBUTTONUP:
                    if frame.buy_button.collidepoint(pygame.mouse.get_pos()):
                        #print(frame.item.name)
                        if not frame.is_bought:

                            if player.buy_item(frame.item): 
                                frame.is_bought = True
                            #font = pygame.font.Font('fonts/8-Bit-Madness.ttf' , 32)
                            #txt = font.render(f"[Bought {frame.item.name.replace('_', ' ').title()}]", True, pygame.Color(0, 0, 0))


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        shop_opened = False

        elif inventory_opened:
            if event.type == pygame.MOUSEBUTTONUP:
                if 50 <= pos[0] <= len(player.rod_inventory)*150 and 100 <= pos[1] <= 200:
                    player.current_rod = player.rod_inventory[((pos[0]-95)//150)]
                    player.image = pygame.transform.scale(chararodarr[player.current_rod], Player.PLAYER_SIZE)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inventory_opened = False
            
        draw_all_text()

                        
                        


        # if event.type == next_background_event:
            # screen.blit(pygame.transform.scale(BACKGROUNDS[background_index%2], (WIDTH, HEIGHT)), (0, 0))
            # background_index += 1
        
    if rng_chance(50) and player.bobber.is_cast and not player.has_fish:
        player.has_fish = True
        sprites.add(meter, meter.bar)
        text_list = []
        drawtext("- Fish on the line -",32, dblue ,610,215, duration=3000)
        #print("- Fish on the line -")
    
    if rng_chance(60) and player.has_fish:
        player.has_fish = False
        text_list = []
        drawtext("- Fish was lost -",32, dblue ,610,215, duration=3000)
        #print("- Fish was lost -")
    
    
    screen.blit(proportional_background, (0, 0))
    sprites.update()
    draw_all_text()

    if True not in (shop_opened, inventory_opened):
        
        sprites.draw(screen)

        if player.menu_opened:
            text_list = []
            player.open_menu(screen)
        else:
            player.close_menu()

        for button in buttons:
            button.draw(screen)

        if player.bobber.is_cast:
            drawtext('[Rod Casted]', 16, pygame.Color(0, 0, 0), WIDTH-100, HEIGHT-20)
        
        static_draw_text("Powerups and Rods:", 18, pygame.Color(0, 0, 0), WIDTH-180, 20)
        inventory = player.powerupstat + player.rod_inventory

        if len(inventory) == 0:
            font = pygame.font.Font('src/img/mariofont.ttf', 16)
            txt = font.render("[Empty]", True, pygame.Color(0, 0, 0))
            _rect = txt.get_rect()
            rect = pygame.Rect(WIDTH-280, 35, _rect.width, _rect.height)
            screen.blit(txt, rect)

        for i, item in enumerate(inventory):
            #static_draw_text(f"-{item}", 16, pygame.Color(0, 0, 0), WIDTH-100, 300 + 20*i)
            if item in power_up_convert.keys():
                item = power_up_convert[item]

            elif item in rods_convert.keys():
                item = rods_convert[item]
            

            font = pygame.font.Font('src/img/mariofont.ttf', 16)
            txt = font.render(f"-{item}", True, pygame.Color(0, 0, 0))
            _rect = txt.get_rect()
            rect = pygame.Rect(WIDTH-280, 35 + 20*i, _rect.width, _rect.height)
            screen.blit(txt, rect)
        
        draw_all_text()
    
    else:
        screen.blit(proportional_background, (0, 0))
        panel_size = (1200, 600)
 
        if shop_opened:
            text_list = []
            shop_menu_panel = pygame.transform.scale(long_menu_image, panel_size)
            screen.blit(shop_menu_panel, (screen.get_width()//2 - panel_size[0]//2, screen.get_height()//2 - panel_size[1]//2))

            for frame in item_frames:
                frame.draw(screen)
        
        elif inventory_opened:
            text_list = []
            cnt = 0   
            panel_size = (1200, 800)

            inventory_menu_panel = pygame.transform.scale(inventorybk, panel_size)
            screen.blit(inventory_menu_panel, (screen.get_width()//2 - panel_size[0]//2, screen.get_height()//2 - panel_size[1]//2 + 50))

            if pygame.time.get_ticks() % 10 == 0 or position_list == [] or len(position_list) < len(player.fish_inventory):
                position_list = [(randint(60, WIDTH-130),randint(HEIGHT-HEIGHT//3, HEIGHT-130)) for fish in player.fish_inventory]

            for i, fish in enumerate(player.fish_inventory):
                print(*position_list[i])
                screen.blit(pygame.transform.scale(fishimgarr[fish.species],(150,100)), position_list[i])

            for i in player.rod_inventory:
                screen.blit(pygame.transform.scale(rodarr[i],(100,100)),(95+140*cnt,100))
            
                cnt +=1
                # Print where the mouse is clicked (for testing purposes)
            if len(player.powerup_inventory) == 1:
                screen.blit(pwruparr[player.powerup_inventory[0]], (850,75))
            if len(player.powerup_inventory) == 2:
                screen.blit(pwruparr[player.powerup_inventory[0]], (850,75))
                screen.blit(pwruparr[player.powerup_inventory[1]], (1050,75))
            if len(player.powerup_inventory) == 3:
                screen.blit(pwruparr[player.powerup_inventory[0]], (850,75))
                screen.blit(pwruparr[player.powerup_inventory[1]], (1050,75))
                screen.blit(pwruparr[player.powerup_inventory[2]], (950,175))

    if not inventory_opened:
        font = pygame.font.Font('src/img/mariofont.ttf', 16)
        txt = font.render(f"Coins: {player.coins}", True, pygame.Color(0, 0, 0))
        _rect = txt.get_rect()
        rect = pygame.Rect(10, 10, _rect.width, _rect.height)
        screen.blit(txt, rect)
    

                
    
    pygame.display.flip()
