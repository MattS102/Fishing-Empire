import pygame
import random
from numpy.random import choice as weighted_choice


class Fish(pygame.sprite.Sprite):
    RARITY_DICT = {  # Dictionary to assign rarity of fish to price
        "Common": 5,
        "Uncommon": 10,
        "Rare": 30,
        "Very Rare": 50,
        "Exotic": 100,
        "Black Market": 200,
    }

    SPECIES_DICT = {
        'bass': 2,
        'cod': 3,
        'trout': 1,
        'salmon': 12,
        'tuna': 15,
        'wincon': 50
    }

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))

        rarity_choice = weighted_choice(  # numpy.random.choice can be used to map a probability array (p) to a value in range(0, 6) corresponding to the RARITY_DICT
            list(range(0, 6)),
            p=[  # Rarity Probabilities (Adds up to 1)
                0.30,  # Common
                0.25,  # Uncommon
                0.20,  # Rare
                0.15,  # Very Rare
                0.075,  # Exotic
                0.025,  # Black Market
            ],
        )

        self.rarity = list(Fish.RARITY_DICT.keys())[
            rarity_choice
        ]  # Set rarity attribute based on rarity choice above

        self.species = random.choice(Fish.SPECIES)


class Player(pygame.sprite.Sprite):
    PLAYER_SIZE = (128, 128)

    PLAYER_IMAGE = pygame.transform.scale(
        pygame.image.load("images/entities/player.png"), PLAYER_SIZE
    )

    SHOP_SIZE = (700, 700)

    SHOP_IMAGE = pygame.transform.scale(
        pygame.image.load("images/menu/menu.png"), SHOP_SIZE
    )


    def __init__(self, position_x, position_y) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.fish_inventory = []
        self.powerup_inventory = []
        self.rod_inventory = []
        self.position = (position_x, position_y)
        self.direction = 0
        self.rect = pygame.Rect(*self.position, *Player.PLAYER_SIZE)
        self.image = Player.PLAYER_IMAGE.copy()

        self.shop_opened = False

        self.bobber = self.Bobber(self)


    def update(self):
        # self.rotate(45)
        pass

    def rotate(self, angle):
        self.image = pygame.transform.rotate(Player.PLAYER_IMAGE, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def open_shop(self, screen):

        screen.blit(Player.SHOP_IMAGE, (screen.get_width()//2 - Player.SHOP_SIZE[0]//2, screen.get_height()//2 - Player.SHOP_SIZE[1]//2 - 60))
        self.shop_opened = True
    
    def close_shop(self):
        self.shoped_opened = False
    
    def cast_rod(self, position):
        self.bobber.is_cast = True
        self.bobber.move_to(*position)

    class Bobber(pygame.sprite.Sprite):

        BOBBER_SIZE = (20, 25)

        BOBBER_IMAGE = pygame.transform.scale(
        pygame.image.load("images/player/bobber.png"), BOBBER_SIZE

        )

        def __init__(self, parent):
            pygame.sprite.Sprite.__init__(self)
            self.parent = parent
            self.position = (0, 0)
            self.image = Player.Bobber.BOBBER_IMAGE.copy()
            self.is_cast = False
            self.rect = pygame.Rect(*self.position, *Player.Bobber.BOBBER_SIZE)
        
        def move_to(self, x, y):
            self.position = (x, y)
            self.rect.x, self.rect.y = x, y

        def draw(self, screen):
            if self.is_cast:
                screen.blit(self.image, self.position)


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
