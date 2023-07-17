import pygame
from numpy.random import choice as weighted_choice


class Fish(pygame.sprite.Sprite):
    RARITY_DICT = {
        "Common": 5,
        "Uncommon": 10,
        "Rare": 30,
        "Very Rare": 50,
        "Exotic": 100,
        "Black Market": 200,
    }

    # Rocket Leauge-type rarity tiers as keys and prices as values

    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))

        rarity_choice = weighted_choice(
            list(range(0, 6)), p=[0.30, 0.25, 0.20, 0.15, 0.075, 0.025]
        )

        self.rarity = list(Fish.RARITY_DICT.keys())[rarity_choice]


class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.inventory = []
