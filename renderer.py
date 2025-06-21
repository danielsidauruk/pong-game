import pygame
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, DARK_SLATE, GOLDEN_YELLOW, 
                      LIME_GREEN, PLAYER_COLOR, AI_COLOR, ELECTRIC_PURPLE, MINT_GREEN)

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.big_font = pygame.font.Font(None, 72)
    
    def draw_background(self):
        """Draw modern animated background"""
        self.screen.fill(DARK_SLATE)
        
        # Draw center line with modern styling
        for i in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.rect(self.screen, WHITE, 
                           (SCREEN_WIDTH // 2 - 2, i, 4, 10))
    
    def draw_name_input_screen(self, input_text):
        """Draw name input screen with modern colors"""
        self.screen.fill(DARK_SLATE)
        
        title_text = self.big_font.render("COLORFUL PONG", True, GOLDEN_YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        prompt_text = self.font.render("Enter your name:", True, WHITE)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(prompt_text, prompt_rect)
        
        # Input box with modern styling
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 50)
        pygame.draw.rect(self.screen, ELECTRIC_PURPLE, input_box, 3)
        
        input_surface = self.font.render(input_text, True, WHITE)
        self.screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))
        
        instruction_text = self.font.render("Press ENTER to start", True, LIME_GREEN)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_game_screen(self, player_paddle, ai_paddle, ball, player_name, player_score, ai_score):
        """Draw game screen"""
        self.draw_background()
        
        # Draw game objects
        player_paddle.draw(self.screen)
        ai_paddle.draw(self.screen)
        ball.draw(self.screen)
        
        # Draw scores with modern colors
        player_text = self.font.render(f"{player_name}: {player_score}", True, PLAYER_COLOR)
        ai_text = self.font.render(f"AI: {ai_score}", True, AI_COLOR)
        
        self.screen.blit(player_text, (50, 30))
        ai_text_rect = ai_text.get_rect()
        ai_text_rect.topright = (SCREEN_WIDTH - 50, 30)
        self.screen.blit(ai_text, ai_text_rect)
        
        # Draw speed indicator
        speed_text = self.font.render(f"Speed: {ball.speed:.1f}", True, WHITE)
        speed_rect = speed_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(speed_text, speed_rect)
    
    def draw_game_over_screen(self, player_name, player_score, ai_score, high_scores):
        """Draw game over screen with modern colors"""
        self.screen.fill(DARK_SLATE)
        
        if player_score > ai_score:
            result_text = self.big_font.render("YOU WIN!", True, LIME_GREEN)
        else:
            result_text = self.big_font.render("AI WINS!", True, AI_COLOR)
        
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(result_text, result_rect)
        
        score_text = self.font.render(f"Final Score - {player_name}: {player_score}, AI: {ai_score}", 
                                    True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(score_text, score_rect)
        
        # Draw high scores with modern styling
        if high_scores:
            high_score_title = self.font.render("HIGH SCORES", True, GOLDEN_YELLOW)
            title_rect = high_score_title.get_rect(center=(SCREEN_WIDTH // 2, 300))
            self.screen.blit(high_score_title, title_rect)
            
            for i, score in enumerate(high_scores[:5]):  # Show top 5
                score_line = f"{i+1}. {score['name']}: {score['score']}"
                score_surface = self.font.render(score_line, True, WHITE)
                score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 340 + i * 30))
                self.screen.blit(score_surface, score_rect)
        
        restart_text = self.font.render("Press SPACE to play again or ESC to quit", True, MINT_GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 520))
        self.screen.blit(restart_text, restart_rect)
