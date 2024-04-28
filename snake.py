"""
Author Paul Brace April 2024
Snake list and elements for Snake game
"""

import pygame
from constants import *
from game_sprite import GameSprite
from sprite_list import SpriteList


snake = SpriteList()

pygame.init()
hit = pygame.mixer.Sound('sounds/lifeLost.wav')
head_up = pygame.image.load('images/headUp.png')
head_down = pygame.image.load('images/headDown.png')
head_left = pygame.image.load('images/headLeft.png')
head_right = pygame.image.load('images/headRight.png')
tail_up = pygame.image.load('images/tailUp.png')
tail_down = pygame.image.load('images/tailDown.png')
tail_left = pygame.image.load('images/tailLeft.png')
tail_right = pygame.image.load('images/tailRight.png')
top_left = pygame.image.load('images/topLeft.png')
top_right = pygame.image.load('images/topRight.png')
bottom_left = pygame.image.load('images/bottomLeft.png')
bottom_right = pygame.image.load('images/bottomRight.png')
horizontal = pygame.image.load('images/horiz.png')
vertical = pygame.image.load('images/vert.png')

# the current direction of travel
current_direction = hold

def initialize_snake():
    global current_direction
    snake.clear_all()
    x = 300
    y = 200
    snake.add(SnakeSegment("head", x, y))
    for i in range(0, 8):
        x += 20
        snake.add(SnakeSegment("body", x, y))
    x += 20
    snake.add(SnakeSegment("tail", x, y))
    current_direction = left


def grow_snake():
    last_index = snake.number() - 1
    # make current tail a cody segment
    snake.items[last_index].type = "body"
    # add a new tail - x and y will be updated on next update
    x = snake.items[last_index].x
    y = snake.items[last_index].y
    snake.add(SnakeSegment("tail", x, y))

def move_snake(direction):
    global current_direction
    if direction != hold:
        head = snake.items[0]

        # move x and y of each segment to that of the previous segment
        for i in range(snake.number() - 1, 0, -1):
            snake.items[i].x = snake.items[i - 1].x
            snake.items[i].y = snake.items[i - 1].y

        # only accept change of direction if not in GRID_WIDTH frame of screen
        if head.x > GRID_WIDTH and head.x < WIDTH - GRID_WIDTH \
            and head.y > GRID_WIDTH and head.y < HEIGHT - GRID_WIDTH:
            if (direction == left and current_direction != right) \
                or (direction == right and current_direction != left) \
                or (direction == up and current_direction != down) \
                or (direction == down and current_direction != up):
                current_direction = direction
        # reposition head
        if current_direction == left:
            snake.items[0].x -= GRID_WIDTH
        elif current_direction == right:
            snake.items[0].x += GRID_WIDTH
        elif current_direction == up:
            snake.items[0].y -= GRID_WIDTH
        elif current_direction == down:
            snake.items[0].y += GRID_WIDTH


        # check if head off screen and enter opposite edge
        if snake.items[0].x < 20:
            snake.items[0].x = WIDTH - GRID_WIDTH
        elif snake.items[0].x > WIDTH - GRID_WIDTH:
            snake.items[0].x = 20
        elif snake.items[0].y < 20:
            snake.items[0].y = HEIGHT - GRID_WIDTH
        elif snake.items[0].y > HEIGHT - GRID_WIDTH:
            snake.items[0].y = 20

        # Set images for direction and turning corner
        for i, segment in enumerate(snake.items):
            # Point head in direction of movement
            if segment.type == "head":
                if current_direction == up:
                    segment.image = head_up
                elif current_direction == down:
                    segment.image = head_down
                elif current_direction == left:
                    segment.image = head_left
                else:
                    segment.image = head_right
            # Point tail in direction of movement
            elif segment.type == "tail":
                dX = segment.x - snake.items[i - 1].x
                dY = segment.y - snake.items[i - 1].y
                if dX != 0:
                    if (dX > 0):
                        #Moving left
                        segment.image = tail_left
                    else:
                        #moving right
                        segment.image = tail_right
                elif dY != 0:
                    if (dY > 0):
                        #Moving down
                        segment.image = tail_up
                    else:
                        #moving up
                        segment.image = tail_down
            else:
                # Body segment so with vertical or horizontal or turning a corner
                nextX = segment.x - snake.items[i - 1].x
                nextY = segment.y - snake.items[i - 1].y
                lastX = segment.x - snake.items[i + 1].x
                lastY = segment.y - snake.items[i + 1].y
                if lastX != 0 and nextX != 0:
                    # Moving horizontally
                    segment.image = horizontal
                elif lastY != 0 and nextY != 0:
                    # Moving vertically
                    segment.image = vertical
                else:
                    # turning a corner the or is to test if coming from edge
                    fromLeft = lastX > 0
                    fromRight = lastX < 0
                    fromDown = lastY < 0
                    fromUp = lastY > 0
                    toLeft = nextX > 0
                    toRight = nextX < 0
                    toUp = nextY > 0
                    toDown = nextY < 0
                    if (fromLeft and toUp) or (fromUp and toLeft):
                        # Bottom right corner
                        segment.image = bottom_right
                    elif (fromDown and toRight) or (fromRight and toDown):
                        # Top left corner
                        segment.image = top_left
                    elif (fromLeft and toDown) or (fromDown and toLeft):
                        # Top right corner
                        segment.image = top_right
                    elif (fromRight and toUp) or (fromUp and toRight):
                        # Bottom left corner
                        segment.image = bottom_left

def draw_smake():
    for snake_segment in snake.items:
        snake_segment.draw()

class SnakeSegment(GameSprite):
    # Snake body elements
    def __init__(self, type, x, y):
        """
        :param type: snake body element type - head, body or tail
        :param x: x coordinate on screen
        :param y: x coordinate on screen
        """
        self.type = type
        if type == "head":
            image = head_left
        elif type == "tail":
            image = tail_left
        else:
            image = horizontal
        super().__init__(image, x, y)

    def hit(self):
        """ snake has hit a bomb or itself """
        self.hit.play()
        self.alive = False
