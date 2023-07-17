import pygame
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

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))

        rarity_choice = weighted_choice(  # numpy.random.choice can be used to map a probability array (p) to a value in range(0, 6)...
            list(range(0, 6)),
            p=[
                0.30,
                0.25,
                0.20,
                0.15,
                0.075,
                0.025,
            ],  # ...this is used to index the RARITY_DICT to assign the self.rarity attribute
        )

        self.rarity = list(Fish.RARITY_DICT.keys())[rarity_choice]  #

        fishesList = ["Cod", "Bass", "Trout", "Salmon", "Tuna"]


class Player(pygame.sprite.Sprite):
    PLAYER_SIZE = (128, 32)

    PLAYER_IMAGE = pygame.transform.scale(
        pygame.image.load("images/entites/direction_test.png"), PLAYER_SIZE
    )

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.inventory = []
        self.position = (640, 360)
        self.direction = 0

        self.rect = pygame.Rect(*self.position, *Player.PLAYER_SIZE)

        self.image = Player.PLAYER_IMAGE.copy()

    def update(self):
        # self.rotate(45)
        pass

    def rotate(self, angle):
        self.image = pygame.transform.rotate(Player.PLAYER_IMAGE, angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class Meter(pygame.sprite.Sprite):
    def __init__(self, position) -> None:
        pygame.sprite.Sprite.__init__(self)

        self.position = position
        self.rect = pygame.Rect(*self.position, 410, 71)
        self.image = pygame.transform.scale(
            pygame.image.load("images/meter/meter.png"),
            (self.rect.width, self.rect.height),
        )
        self.bar = self.Bar(self)

    def update(self):
        self.bar.move()

    class Bar(pygame.sprite.Sprite):
        def __init__(self, parent) -> None:
            pygame.sprite.Sprite.__init__(self)
            self.parent = parent
            self.position = parent.position
            self.rect = pygame.Rect(*self.position, 3, 71)
            self.image = pygame.transform.scale(
                pygame.image.load("images/meter/bar.png"),
                (self.rect.width, self.rect.height),
            )
            self.is_increasing = True

        def move(self):
            change = 20 if self.is_increasing else -20

            if self.parent.rect.x - self.rect.x > -60 and not self.is_increasing:
                self.is_increasing = True

            elif (
                self.parent.rect.x + self.parent.rect.width - self.rect.x < 60
                and self.is_increasing
            ):
                self.is_increasing = False

            self.position = (self.position[0] + change, self.position[1])
            self.rect.x += change
