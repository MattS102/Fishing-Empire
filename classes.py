import pygame
import random
from numpy.random import choice as weighted_choice
from numpy import pi



class Fish(pygame.sprite.Sprite):
    RARITY_DICT = {  # Dictionary to assign rarity of fish to price
        "Common": 5,
        "Uncommon": 10,
        "Rare": 30,
        "Very Rare": 50,
        "Exotic": 100,
        "Black Market": 200,
    }

    RARITY_MULTIPLIER_DICT = {
        10: [0.90, 0.1, 0.0, 0.0, 0.0, 0.0],
        30: [0.70, 0.25, 0.05, 0.0, 0.0, 0.0],
        50: [0.50, 0.20, 0.15, 0.10, 0.05, 0.0],
        70: [0.30, 0.25, 0.25, 0.10, 0.05, 0.05],
        90: [0.15, 0.15, 0.30, 0.15, 0.15, 0.10]
    }

    SPECIES_DICT = {
        'Bass': 2,
        'Cod': 3,
        'Trout': 1,
        'Salmon': 12,
        'Tuna': 15,
        'Wincon': 50
    }


    def __init__(self, rarity_multiplier) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.species = random.choice(list(Fish.SPECIES_DICT.keys()))
        self.image = pygame.image.load(f'images/entities/fish/{self.species.lower()}.png')
        self.rect =  pygame.Rect(0, 0,  *self.image.get_size())

        rarity_multiplier_key = min(Fish.RARITY_MULTIPLIER_DICT.keys(), key=lambda x:abs(x-rarity_multiplier))
        
        rarity_choice = weighted_choice(  # numpy.random.choice can be used to map a probability array (p) to a value in range(0, 6) corresponding to the RARITY_DICT
            list(range(0, 6)),
            p=Fish.RARITY_MULTIPLIER_DICT[rarity_multiplier_key]
        )

        self.rarity = list(Fish.RARITY_DICT.keys())[
            rarity_choice
        ]  # Set rarity attribute based on rarity choice above

        self.name = f"{self.rarity} {self.species}"


    
    def __repr__(self):
        return self.name


class Player(pygame.sprite.Sprite):
    PLAYER_SIZE = (128, 128)

    PLAYER_IMAGE = pygame.transform.scale(
        pygame.image.load("images/entities/player.png"), PLAYER_SIZE
    )

    SHOP_SIZE = (600, 600)

    SHOP_IMAGE = pygame.transform.scale(
        pygame.image.load("images/menu/menu.png"), SHOP_SIZE
    )

    SHOP_PRICES = {"Captain Hooker" : 50, 
                   "Salmon Slayer" : 150, 
                   "Trout Terminator" : 400, 
                   "Aquatic Abductor" : 1000, 
                   "Slow-Time" : 50, 
                   "1 in a Million" : 80, 
                   "Double Down" : 100}


    def __init__(self, screen, position_x, position_y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.fish_inventory = []
        self.powerup_inventory = ["slowtime", "coinup" , "luckup"]
        self.rod_inventory = ["aa", "ch"]
        self.position = (position_x, position_y)
        self.direction = 0
        self.rect = pygame.Rect(*self.position, *Player.PLAYER_SIZE)
        self.image = Player.PLAYER_IMAGE.copy()
        self.coins = 1000

        self.menu_opened = False

        self.bobber = self.Bobber(self)
        self.powerupstat = []
        self.has_fish = False
        self.current_rod = "fs"


    def update(self):
        # self.rotate(45)
        pass

    def rotate(self, angle):
        self.image = pygame.transform.rotate(Player.PLAYER_IMAGE, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def open_menu(self, screen):
        screen.blit(Player.SHOP_IMAGE, (screen.get_width()//2 - Player.SHOP_SIZE[0]//2, screen.get_height()//2 - Player.SHOP_SIZE[1]//2 - 30))
        self.menu_opened = True
    
    def close_menu(self):
        self.menu_opened = False
    
    def cast_rod(self, screen, position):
        self.bobber.move_to(*position)

    def sell_fish(self, species, rarity, quantity):
        sell_queue = []
        new_fish_inventory = []

        for fish in self.fish_inventory:
            if fish.species == species and fish.rarity == rarity:
                sell_queue.append(fish)
            else:
                new_fish_inventory.append(fish)
        
        if len(sell_queue) == quantity:
            self.fish_inventory = new_fish_inventory

            print("Transaction Completed")
        
        else:
            print(f"Transaction Failed: You need {abs(len(sell_queue) - quantity)} more {rarity} {species}")
    
    def buy_item(self, item):

        if self.coins - item.price >= 0:
            self.coins -= item.price 
            self.rod_inventory.append(item)

            print(self.coins)

            return True
        
        else:
            print("Transaction Failed: Insufficient Funds")
            return False
                
            



    class Bobber(pygame.sprite.Sprite):

        BOBBER_SIZE = (20, 25)

        BOBBER_IMAGE = pygame.transform.scale(
        pygame.image.load("images/player/bobber.png"), BOBBER_SIZE

        )

        def __init__(self, parent):
            pygame.sprite.Sprite.__init__(self)
            self.screen = parent.screen
            self.parent = parent
            self.position = (0, 0)
            self.image = Player.Bobber.BOBBER_IMAGE.copy()
            self.is_cast = False
            self.rect = pygame.Rect(*self.position, *Player.Bobber.BOBBER_SIZE)
        
        def move_to(self, x, y):
            self.position = (x, y)
            self.rect.x, self.rect.y = x, y

        def update(self):
            if self.parent.current_rod == 'aa':
                rod_position = (self.parent.position[0]+128, self.parent.position[1]+57)
            else:
                rod_position = (self.parent.position[0]+120, self.parent.position[1]+15)

            bobber_top_position = (self.position[0]+15, self.position[1])
            pygame.draw.line(self.screen, pygame.Color(0, 0, 0, 0), rod_position, bobber_top_position , 3)


class Meter(pygame.sprite.Sprite):

    METER_SIZE = (710, 51)

    def __init__(self, position_x, position_y) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.position = (position_x, position_y)
        self.rect = pygame.Rect(*self.position, *Meter.METER_SIZE)
        self.image = pygame.transform.scale(
            pygame.image.load("images/meter/meter.png"),
            (self.rect.width, self.rect.height),
        )
        self.bar = self.Bar(self)
        self.stopped = False
        self.percentage = self.bar.percentage
    
    def draw(self, screen):
        screen.blit(self.image, self.position)

    def update(self):
        self.stopped = self.bar.stopped
        self.percentage = self.bar.percentage
        self.bar.update()
    
    def reset(self):
        self.bar.reset()

    class Bar(pygame.sprite.Sprite):
        def __init__(self, parent) -> None:
            pygame.sprite.Sprite.__init__(self)
            self.parent = parent
            self.position = (self.parent.rect.x + self.parent.rect.width * (4 / 82), self.parent.rect.y)
            self.rect = pygame.Rect(*self.position, 3, parent.rect.height)
            self.image = pygame.transform.scale(
                pygame.image.load("images/meter/bar.png"),
                (self.rect.width, self.rect.height),
            )
            self.is_increasing = True
            self.percentage = 0 
            self.current = 0
            self.stopped = False

        def move(self):
            speed = 25
            start = self.parent.rect.x + self.parent.rect.width * (6 / 82)
            end = self.parent.rect.x + self.parent.rect.width - self.parent.rect.width * (6 / 82)
            self.percentage = (self.rect.x + 2 - start) / (end - start) * 100

            step = speed * (1 if self.is_increasing else -1)

            
            if start - self.rect.x > step and not self.is_increasing:
                self.is_increasing = True
            
            if end - self.rect.x < step and self.is_increasing:
                self.is_increasing = False


            step = speed * (1 if self.is_increasing else -1)


            self.position = (self.position[0] + step, self.position[1])
            self.rect.x += step

        def draw(self, screen):
            screen.blit(self.image, self.position)
        
        def update(self):
            if not self.stopped:
                self.move()
        
        def reset(self):

            self.position = (self.parent.rect.x + self.parent.rect.width * (4 / 82), self.parent.rect.y)
            self.rect = pygame.Rect(*self.position, 3, self.parent.rect.height)
            self.stopped = False

class Button(pygame.sprite.Sprite):

    def __init__(self, text, x, y, width, height, clicked_function, button_type='long', font_size=32) -> None:

        pygame.sprite.Sprite.__init__(self)
        
        self.font_size = font_size
        self.position = (x-width/2, y-height//2)
        self.rect = pygame.Rect(x-width//2, y-height//2, width, height)
        self.image = pygame.transform.scale(pygame.image.load(f"images/menu/{button_type}_button.png"), (width, height))
        self.text = text
        self.clicked = False
    

    def draw(self, screen):
        font = pygame.font.Font('fonts/8-Bit-Madness.ttf', self.font_size)
        text = font.render(self.text, True, pygame.Color(0, 0, 0))
        rect = text.get_rect()
        rect.center = (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2) 
        screen.blit(self.image, self.position)
        screen.blit(text, rect)


class ItemFrame(pygame.sprite.Sprite):
    
    def __init__(self, item,  x, y, quantity=1):
        self.rect = pygame.Rect(x, y, 170, 200)
        self.position = (x//2, y//2)
        self.image = pygame.Surface((170, 200))
        self.item = item
        self.quantity = quantity
        self.buy_button = pygame.Rect(x, y + 155, 170, 45)
        self.is_bought = False
        
    def __repr__(self):
        return f"Item Frame holding x{self.quantity} {self.item}"

    def draw(self, screen):

        image_rect = self.image.get_rect()
        item_rect = self.item.image.get_rect()

        pygame.draw.rect(self.image, pygame.Color(255, 255, 255), image_rect, 1)
        pygame.draw.line(self.image, pygame.Color(255, 255, 255), (image_rect.x, image_rect.y + 155), (image_rect.x + image_rect.width, image_rect.y + 155))
        self.image.blit(pygame.transform.scale(self.item.image, Player.PLAYER_SIZE), (image_rect.x + image_rect.width//2 - item_rect.width - 30, image_rect.y + image_rect.height//2 - item_rect.height - 50))

        font = pygame.font.Font('fonts/8-Bit-Madness.ttf', 16)

        if not self.is_bought:
            text1 = font.render(f"Buy {self.item.name.replace('_', ' ').title()}", True, pygame.Color(255, 255, 255))
            text1_rect = text1.get_rect()
            self.image.blit(text1, (image_rect.x+image_rect.width//2-text1_rect.width//2, image_rect.y+image_rect.height-text1_rect.height//2-25))
        
            text2 =  font.render(f"for ${self.item.price}", True, pygame.Color(255, 255, 255))
            text2_rect = text2.get_rect()
            self.image.blit(text2, (image_rect.x+image_rect.width//2-text2_rect.width//2, image_rect.y+image_rect.height-text2_rect.height//2-15))

        else:
            text1 = font.render(f"[ Owned ]", True, pygame.Color(255, 255, 255))
            text1_rect = text1.get_rect()
            self.image.blit(text1, (image_rect.x+image_rect.width//2-text1_rect.width//2, image_rect.y+image_rect.height-text1_rect.height//2-25))
        
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Item(pygame.sprite.Sprite):
    
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.image = pygame.image.load(f'images/player/{name}.png')