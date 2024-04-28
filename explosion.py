"""
Author Paul Brace April 2024
Explosion class for Python games
"""

import pygame
import random
from sprite_list import SpriteList

explosions = SpriteList()
pygame.init()
bang = pygame.mixer.Sound('sounds/strike.wav')

class Explosion:
    def __init__(self, x_pos, y_pos, size, color, rate):
        """
        :param x_pos: x screen coordinate
        :param y_pos: y screen coordinate
        :param size: number of particles that will be created for the explosion e.g. 50
        :param color: the color of the explosion particles
        :param rate: the rate at which the particles will reduce in size and then disappear
                    try 0.025 to 0.05
        """
        self.x = x_pos
        self.y = y_pos
        self.size = size
        self.color = color
        self.rate = rate
        self.done = False
        self.particles = []
        self.explode()

    def update(self):
        for particle in self.particles:
            particle.update()
            if particle.done:
                self.particles.remove(particle)
        if len(self.particles) == 0:
            self.done = True

    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

    def explode(self):
        # Create an explosion effect
        # create particles
        bang.play()
        for i in range(0, self.size * 2):
            self.particles.append(Particle(self.x, self.y,
                                           random.random() * 4,
                                           self.color,
                                           (random.random() - 0.5) * random.random() * 6,
                                           (random.random() - 0.5) * random.random() * 6,
                                           self.rate))


FRICTION = 0.99


class Particle:
    def __init__(self, x, y, radius, color, velocity_x, velocity_y, rate):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.rate = rate
        self.alpha = 1
        self.done = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update(self):
        self.velocity_x *= FRICTION
        self.velocity_y *= FRICTION
        if self.radius > 0:
            self.radius -= self.rate
        if self.radius <= 0:
            self.done = True
        if not self.done:
            # change velocity
            self.x += self.velocity_x
            self.y += self.velocity_y
