import pygame
import random
import os

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        paddle_sound_path = "assets/paddle_hit.wav"
        wall_sound_path = "assets/wall_bounce.wav"
        self.paddle_hit_sound = pygame.mixer.Sound(paddle_sound_path)
        self.wall_bounce_sound = pygame.mixer.Sound(wall_sound_path)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            self.wall_bounce_sound.play()



    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def check_collision(self, player, ai):
        # Create Rect objects for this frame
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()

        if ball_rect.colliderect(player_rect):
            # Only trigger if the ball is moving towards the player
            if self.velocity_x < 0:
                self.velocity_x *= -1
                # Place the ball just to the right of the player's paddle
                self.x = player_rect.right
                self.paddle_hit_sound.play()

        # Check collision with the AI's paddle (right side)
        if ball_rect.colliderect(ai_rect):
            # Only trigger if the ball is moving towards the AI
            if self.velocity_x > 0:
                self.velocity_x *= -1
                # Place the ball just to the left of the AI's paddle
                self.x = ai_rect.left - self.width
                self.paddle_hit_sound.play()
