"""
Author Paul Brace April 2024
Snake game developed using PyGame
Music Monkeys Spinning Monkeys by Kevin MacLeod
"""

import pygame
import random
from constants import *
from snake import *
from target import Target, targets
from score_board import ScoreBoard
from explosion import Explosion, explosions
from sprite_list import SpriteList

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
running = True

score_board = ScoreBoard()
score_board.lives = START_LIVES
score_board.load_high_score()

music = pygame.mixer.Sound('sounds/SnakeTune.mp3')
music.set_volume(0.25)
game_over = pygame.mixer.Sound('sounds/GameOver.wav')
bonus_sweets = pygame.mixer.Sound('sounds/sweets.wav')

# direction selected by player
direction = hold
# Timer for number of frames to pause between snake update
refresh_timer = 0
snake_speed = REFRESH_DELAY

def get_pos():
    # get a random grid position
    x = random.randint(GRID_WIDTH * 2, WIDTH - GRID_WIDTH * 2)
    x = round(x / GRID_WIDTH) * GRID_WIDTH
    y = random.randint(GRID_WIDTH * 3, HEIGHT - GRID_WIDTH * 2)
    y = round(y / GRID_WIDTH) * GRID_WIDTH
    return x, y

def occupied(x, y):
    # checks if the x, y position is currently occupied by a target
    taken = False
    for target in targets.items:
        if target.x == x and target.y == y:
            taken = True
    if not taken:
        # check if position occupied by part of the snake body
        for segment in snake.items:
            if segment.x == x and segment.y == y:
                taken = True
    return taken

def add_target(type):
    """
    :param type: 'apple', 'bomb' or 'sweet'
    :return:
    """
    x, y = get_pos()
    while (occupied(x, y)):
        x, y = get_pos()
    targets.add(Target(type, x, y))

def add_sweets():
    bonus_sweets.play()
    n = random.randint(2, 5)
    for _ in range(2, 5):
        add_target("sweet")


def start_game():
    global direction
    # Called at the beginning of each life
    # clear all objects
    targets.clear_all()
    explosions.clear_all()
    # Clear game objects
    initialize_snake()
    add_target("apple")
    add_target("bomb")
    direction = hold

start_game()

def clear_done_objects():
    targets.clear_done()
    explosions.clear_done()

def get_direction(direction):
    # Check keyboard for player instructions
    if score_board.game_state != GAME_OVER:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            direction = left
        if keys[pygame.K_RIGHT]:
            direction = right
        if keys[pygame.K_UP]:
            direction = up
        if keys[pygame.K_DOWN]:
            direction = down
        return direction

def update_game():
    global direction, refresh_timer, snake_speed

    # Check for end of game
    if (snake.items[0].done) and explosions.number() == 0:
        if score_board.lives < 1:
            score_board.game_state = GAME_OVER
            music.stop()
            game_over.play()
        else:
            start_game()
        return

    clear_done_objects()

    for explosion in explosions.items:
        explosion.update()

    direction = get_direction(direction)
    refresh_timer += 1
    if refresh_timer >= snake_speed and direction != hold and not snake.items[0].done:
        move_snake(direction)
        refresh_timer = 0

    hit = False
    # Check if hit any targets
    for target in targets.items:
        target.update()
        if snake.items[0].collide_rect(target):
            target.eaten()
            if target.type == "bomb":
                explosions.add(Explosion(target.x, target.y, 50, "darkgray", 0.025))
                score_board.lives -= 1
                snake.items[0].done = True
                direction = hold
            else:
                hit = True
                score_board.score += target.points
                grow_snake()
                if target.type == "apple":
                    add_target("apple")
    if hit:
        if score_board.score % 25 == 0:
            add_target("bomb")
        if score_board.score % 50 == 0:
            add_sweets()
        if score_board.score % 200 == 0 and snake_speed > 4:
            # Reduce delay between refreshing the snake
            snake_speed -= 1
    # Check if head has hit any other part of the snake
    if not snake.items[0].done:
        head = snake.items[0]
        for segment in snake.items:
            if segment.type != "head":
                if head.collide_rect(segment):
                    explosions.add(Explosion(head.x, head.y, 50, "green", 0.025))
                    score_board.lives -= 1
                    snake.items[0].done = True
                    direction = hold

def draw_game_screen():
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    snake.draw(screen)
    targets.draw(screen)
    explosions.draw(screen)
    score_board.draw(screen)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X so end game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #clear_done_objects()
    if score_board.game_state == INPLAY or explosions.number() > 0:
        update_game()
        draw_game_screen()
    elif score_board.game_state == GAME_OVER:
        start, play = score_board.draw_game_over(screen)
        if start == "start":
            # Reset snake speed
            snake_speed = REFRESH_DELAY
            score_board.score = 0
            score_board.level = 1
            score_board.lives = START_LIVES
            score_board.game_state = INPLAY
            if play == "music":
                music.play(-1)
            start_game()
    else:
        start, play = score_board.draw_game_instructions(screen)
        if  start == "start":
            snake_speed = REFRESH_DELAY
            score_board.game_state = INPLAY
            if play == "music":
                music.play(-1)
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()