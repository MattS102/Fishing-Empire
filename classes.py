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
    
    def __repr__(self):
        return f"{self.rarity} {self.species}"


class Player(pygame.sprite.Sprite):
    PLAYER_SIZE = (128, 128)

    PLAYER_IMAGE = pygame.transform.scale(
        pygame.image.load("images/entities/player.png"), PLAYER_SIZE
    )

    SHOP_SIZE = (600, 600)

    SHOP_IMAGE = pygame.transform.scale(
        pygame.image.load("images/menu/menu.png"), SHOP_SIZE
    )


    def __init__(self, screen, position_x, position_y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.fish_inventory = []
        self.powerup_inventory = []
        self.rod_inventory = []
        self.position = (position_x, position_y)
        self.direction = 0
        self.rect = pygame.Rect(*self.position, *Player.PLAYER_SIZE)
        self.image = Player.PLAYER_IMAGE.copy()

        self.menu_opened = False

        self.bobber = self.Bobber(self)

        self.has_fish = False


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
        self.shoped_opened = False
    
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
            rod_postion = (self.parent.position[0]+120, self.parent.position[1]+15)
            bobber_top_position = (self.position[0]+15, self.position[1])
            pygame.draw.line(self.screen, pygame.Color(0, 0, 0, 0), rod_postion, bobber_top_position , 3)


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
        self.clicked_function = clicked_function
    

    def draw(self, screen):
        font = pygame.font.Font('fonts/8-Bit-Madness.ttf', self.font_size)
        text = font.render(self.text, True, pygame.Color(0, 0, 0))
        rect = text.get_rect()
        rect.center = (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2) 
        screen.blit(self.image, self.position)
        screen.blit(text, rect)

    def click_handler(self):
        self.clicked_function('hello')

