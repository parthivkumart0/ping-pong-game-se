import pygame
import random

class Paddle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7
        self.mistake_chance = 0.02

    def move(self, dy, screen_height):
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        if random.random() > self.mistake_chance:
            if ball.y < self.y:
                self.move(-self.speed, screen_height)
            elif ball.y > self.y + self.height:
                self.move(self.speed, screen_height)
        else:
            random_direction = random.choice([-self.speed, self.speed])
            self.move(random_direction, screen_height)
