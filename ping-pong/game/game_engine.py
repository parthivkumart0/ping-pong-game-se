import pygame
from .paddle import Paddle
from .ball import Ball
WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)
        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        
        self.winning_score = 5
        self.game_over = False
        score_sound_path = "assets/score_point.wav"
        self.score_sound = pygame.mixer.Sound(score_sound_path)
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        if self.ball.x <= 0:
            self.ai_score += 1
            if self.score_sound: #score sound
                self.score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            if self.score_sound: # score sound
                self.score_sound.play()
            self.ball.reset()if self.ball.x <= 0:
            self.ai_score += 1
            if self.score_sound: #score sound
                self.score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            if self.score_sound: # score sound
                self.score_sound.play()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)
        
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            self.game_over = True

    def render(self, screen):
        if self.game_over:
            winner_text_str = "Player Wins!" if self.player_score >= self.winning_score else "AI Wins!"
        
            # --- Draw Winner Text ---
            winner_font = pygame.font.SysFont("Arial", 50) # A larger font for the winner
            winner_surface = winner_font.render(winner_text_str, True, WHITE)
            winner_rect = winner_surface.get_rect(center=(self.width // 2, self.height // 2 - 100))
            screen.blit(winner_surface, winner_rect)
            
            score_font = pygame.font.SysFont("Arial", 30) # A medium font for the score
            final_score_str = f"AI: {self.ai_score} v/s Player: {self.player_score}"
            final_score_surface = score_font.render(final_score_str, True, WHITE)
            # Position the score 60 pixels below the winner text
            final_score_rect = final_score_surface.get_rect(center=(self.width // 2, winner_rect.centery + 60))
            screen.blit(final_score_surface, final_score_rect)

            # --- Draw Replay Options ---
            options_font = pygame.font.SysFont("Arial", 24) # A smaller font for options
            options = [
                "Play Again:",
                "Best of 3 (Press 3)",
                "Best of 5 (Press 5)",
                "Best of 7 (Press 7)",
                "Exit (Press ESC)"
            ]
        
            # Draw each line of text, stacked vertically
            for i, option in enumerate(options):
                option_surface = options_font.render(option, True, WHITE)
                option_rect = option_surface.get_rect(center=(self.width // 2, self.height // 2 + i * 40))
                screen.blit(option_surface, option_rect)
        else:
            # Your existing render code goes here, indented
            
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width//4, 20))
            screen.blit(ai_text, (self.width * 3//4, 20))
            
    def reset_game(self, best):
        self.player_score = 0
        self.ai_score = 0
        self.winning_score = (best//2) + 1
        self.game_over = False
        self.ball.reset()
        
       
