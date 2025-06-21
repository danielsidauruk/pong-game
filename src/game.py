import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, PLAYER_COLOR, AI_COLOR
from paddle import Paddle
from ball import Ball
from ai_player import AIPlayer
from sound_manager import SoundManager
from score_manager import ScoreManager
from input_handler import InputHandler
from renderer import Renderer

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        
        # Initialize managers
        self.sound_manager = SoundManager()
        self.score_manager = ScoreManager()
        self.input_handler = InputHandler()
        self.renderer = Renderer(self.screen)
        
        # Initialize game objects
        self.player_paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PLAYER_COLOR)
        self.ai_paddle = Paddle(SCREEN_WIDTH - 30 - PADDLE_WIDTH, 
                               SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, AI_COLOR)
        self.ball = Ball()
        self.ai_player = AIPlayer(self.ai_paddle, difficulty=0.7)
        
        # Game state
        self.player_score = 0
        self.ai_score = 0
        self.player_name = ""
        self.game_state = "name_input"  # "name_input", "playing", "game_over"
        self.input_text = ""
    
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.game_state == "name_input":
                self.input_text, should_start = self.input_handler.handle_name_input(event, self.input_text)
                if should_start:
                    self.player_name = self.input_text
                    self.game_state = "playing"
                    
            elif self.game_state == "game_over":
                action = self.input_handler.handle_game_over_input(event)
                if action == "restart":
                    self.restart_game()
                elif action == "quit":
                    return False
        
        return True
    
    def handle_input(self):
        """Handle continuous input (paddle movement)"""
        if self.game_state == "playing":
            self.input_handler.handle_paddle_movement(self.player_paddle)
    
    def update_game(self):
        """Update game logic"""
        if self.game_state != "playing":
            return
        
        # Move ball
        self.ball.move()
        
        # Update AI
        self.ai_player.update(self.ball)
        
        # Ball collision with top/bottom walls
        from constants import BALL_SIZE
        if self.ball.y <= BALL_SIZE or self.ball.y >= SCREEN_HEIGHT - BALL_SIZE:
            self.ball.bounce_y()
            self.sound_manager.play('bounce')
        
        # Ball collision with paddles
        ball_rect = self.ball.get_rect()
        player_rect = self.player_paddle.get_rect()
        ai_rect = self.ai_paddle.get_rect()
        
        if ball_rect.colliderect(player_rect) and self.ball.dx < 0:
            self.ball.bounce_x()
            self.sound_manager.play('bounce')
        elif ball_rect.colliderect(ai_rect) and self.ball.dx > 0:
            self.ball.bounce_x()
            self.sound_manager.play('bounce')
        
        # Ball goes off screen (scoring)
        if self.ball.x < 0:
            self.ai_score += 1
            self.sound_manager.play('score')
            self.ball.reset()
            if self.ai_score >= 10:  # Game ends at 10 points
                self.game_state = "game_over"
                self.score_manager.add_high_score(self.player_name, self.player_score)
        elif self.ball.x > SCREEN_WIDTH:
            self.player_score += 1
            self.sound_manager.play('score')
            self.ball.reset()
            if self.player_score >= 10:  # Game ends at 10 points
                self.game_state = "game_over"
                self.score_manager.add_high_score(self.player_name, self.player_score)
    
    def render(self):
        """Render the current game state"""
        if self.game_state == "name_input":
            self.renderer.draw_name_input_screen(self.input_text)
        elif self.game_state == "playing":
            self.renderer.draw_game_screen(
                self.player_paddle, self.ai_paddle, self.ball,
                self.player_name, self.player_score, self.ai_score
            )
        elif self.game_state == "game_over":
            self.renderer.draw_game_over_screen(
                self.player_name, self.player_score, self.ai_score,
                self.score_manager.get_high_scores()
            )
    
    def restart_game(self):
        """Restart the game"""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_state = "name_input"
        self.input_text = ""
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_events()
            self.handle_input()
            self.update_game()
            self.render()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
