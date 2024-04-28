"""
Author Paul Brace April 2024
ScoreBoard class for Snake game
"""

import pygame
import constants as const

pygame.init()
font = "veranda"
heading = pygame.font.SysFont(font, 50, False, False)
text = pygame.font.SysFont(font, 30, False, False)
italic = pygame.font.SysFont(font, 30, False, True)
bold = pygame.font.SysFont(font, 30, True, False)
small = pygame.font.SysFont(font, 20, False, False)
scores = pygame.font.SysFont("freesans", 15, True, False)

instructions = ["Press left, right up and down arrow to move",
                "Eat food to score",
                "Watch out for sweets, they do not last long",
                "Eating a bomb or the snake body looses a life",
                "Score for eating apples = 5 sweets = 15",
                "Snake gets longer the more you eat",
                "The snake gets quicker the longer you play"]

class ScoreBoard():
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.high_saved = False
        self.lives = 0
        self.life_image = pygame.image.load('images/life.png')
        self.game_state = const.PAUSED

    def load_high_score(self):
        try:
            with open("scores.txt", "r") as file:
                self.high_score = int(file.read())
        except:
            self.high_score = 0

    def draw_text(self, screen, text, pos, font, color):
        label = font.render(text, False, color)
        screen.blit(label, pos)
        return label.get_height() * 2

    def draw_text_center(self, screen, text, pos, font, color):
        label = font.render(text, False, color)
        cent_pos = (pos[0] - label.get_width() / 2, pos[1])
        screen.blit(label, cent_pos)
        return label.get_height() * 2

    def draw(self, screen):
        self.draw_text(screen, f"Your score: {self.score}", (20, 10),
                         scores,"white"),
        self.draw_text(screen, f"High score: {self.high_score}", (200, 10),
                         scores, "white")
        """ draw an image for each life remaining """
        for i in range(self.lives):
            screen.blit(self.life_image, (i * 35 + 680, 10))

    def draw_game_over(self, screen):
        self.draw_text_center(screen, "Game over",  (400, 100),
                              heading,"yellow")
        self.draw_text_center(screen, f"Your score: {self.score}", (400, 250),
                         heading, "white")
        if self.score > self.high_score:
            # high_score = Player.score
            self.draw_text_center(screen, "Congratulations a new high score!", (400, 360),
                             heading, "green")
            if not self.high_saved:
                # save high score
                with open("scores.txt", "w") as file:
                    file.write(str(self.score))
                self.high_saved = True
        self.draw_text_center(screen, "Press space bar for another game",  (400, 475),
                        text,"aqua")
        self.draw_text_center(screen, "Press M to start with music", (400, 515),
                              text, "aqua")
        self.draw_text_center(screen, "Author: Paul Brace 2024", (400, 550),
                              small, "white")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return "start", "silent"
        elif keys[pygame.K_m]:
            return "start", "music"
        else:
            return "", ""
    def draw_game_instructions(self, screen):
        y = 50
        self.draw_text_center(screen, "Snake - Instructions",  (400, y),
                              heading, "yellow")
        y = 150
        for line in instructions:
            y += self.draw_text(screen, line, (175, y), text, "white")
        y += self.draw_text_center(screen, "Press space bar to start with no music", (400, 475),
                              text, "aqua")
        self.draw_text_center(screen, "Press M to start with music", (400, 515),
                              text, "aqua")
        self.draw_text_center(screen, "Author: Paul Brace 2024", (400, 550),
                              small, "white")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            return "start", "silent"
        elif keys[pygame.K_m]:
            return "start", "music"
        else:
            return "", ""