"""
Author Paul Brace April 2024
Target class for Snake game
"""

import pygame
from constants import *
from game_sprite import GameSprite
from sprite_list import SpriteList
import random

pygame.init()
eat = pygame.mixer.Sound('sounds/crunch.wav')
apple = pygame.image.load("images/apple.png")
bomb = pygame.image.load("images/bomb.png")
sweet_images = []
sweet_images.append(pygame.image.load("images/sweet1.png"))
sweet_images.append(pygame.image.load("images/sweet2.png"))
sweet_images.append(pygame.image.load("images/sweet3.png"))
sweet_images.append(pygame.image.load("images/sweet4.png"))

targets = SpriteList()

class Target(GameSprite):
    def __init__(self, type, x, y):
        """
        :param type: Type of taget - apple, bomb or sweet
        :param x: x coordinate on screen
        :param y: y coordinate on screen
        """
        self.type = type
        if type == "apple":
            image = apple
            self.points = 5
        elif type == "bomb":
            image = bomb
            self.points = 0
        else:
            image = sweet_images[random.randint(0, 3)]
            self.points = 15
        super().__init__(image, x, y)
        self.timer = DISPLAY_SWEET

    def eaten(self):
        if self.type != "bomb":
            eat.play()
        self.done = True
        return self.points


    def update(self):
        # remove sweet after timer frames
        if self.type == "sweet":
            self.timer -= 1
        if self.timer <= 0:
            self.done = True
