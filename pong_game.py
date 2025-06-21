import pygame
import random
import math
import json
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15
PADDLE_SPEED = 8
INITIAL_BALL_SPEED = 6
SPEED_INCREMENT = 0.2
MAX_BALL_SPEED = 12

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 191, 255)
NEON_GREEN = (57, 255, 20)
NEON_PINK = (255, 20, 147)
NEON_ORANGE = (255, 165, 0)
NEON_PURPLE = (138, 43, 226)
NEON_YELLOW = (255, 255, 0)
NEON_RED = (255, 0, 0)
DARK_BLUE = (0, 0, 139)

# Ball colors for cycling
BALL_COLORS = [NEON_BLUE, NEON_GREEN, NEON_PINK, NEON_ORANGE, NEON_PURPLE, NEON_YELLOW, NEON_RED]

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.create_sounds()
    
    def create_sounds(self):
        """Create simple sound effects using pygame's sound generation"""
        try:
            # Create bounce sound (short beep)
            bounce_sound = pygame.sndarray.make_sound(
                self.generate_tone(440, 0.1, 44100)
            )
            self.sounds['bounce'] = bounce_sound
            
            # Create score sound (higher pitch)
            score_sound = pygame.sndarray.make_sound(
                self.generate_tone(880, 0.3, 44100)
            )
            self.sounds['score'] = score_sound
            
        except:
            # If sound generation fails, create dummy sounds
            self.sounds['bounce'] = None
            self.sounds['score'] = None
    
    def generate_tone(self, frequency, duration, sample_rate):
        """Generate a simple sine wave tone"""
        import numpy as np
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            wave = 4096 * math.sin(frequency * 2 * math.pi * i / sample_rate)
            arr[i][0] = wave
            arr[i][1] = wave
        
        return arr.astype(pygame.int16)
    
    def play(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass

class Paddle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = color
        self.speed = PADDLE_SPEED
        
    def move_up(self):
        if self.y > 0:
            self.y -= self.speed
    
    def move_down(self):
        if self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
    
    def draw(self, screen):
        # Draw paddle with glow effect
        glow_rect = pygame.Rect(self.x - 2, self.y - 2, self.width + 4, self.height + 4)
        pygame.draw.rect(screen, (self.color[0]//3, self.color[1]//3, self.color[2]//3), glow_rect)
        
        paddle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, paddle_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Ball:
    def __init__(self):
        self.reset()
        self.color_index = 0
        
    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed = INITIAL_BALL_SPEED
        
        # Random direction
        angle = random.uniform(-math.pi/4, math.pi/4)
        if random.choice([True, False]):
            angle += math.pi
        
        self.dx = self.speed * math.cos(angle)
        self.dy = self.speed * math.sin(angle)
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def bounce_y(self):
        self.dy = -self.dy
        self.change_color()
    
    def bounce_x(self):
        self.dx = -self.dx
        self.change_color()
        # Increase speed slightly
        if self.speed < MAX_BALL_SPEED:
            self.speed += SPEED_INCREMENT
            # Maintain direction but increase magnitude
            speed_ratio = self.speed / math.sqrt(self.dx**2 + self.dy**2)
            self.dx *= speed_ratio
            self.dy *= speed_ratio
    
    def change_color(self):
        self.color_index = (self.color_index + 1) % len(BALL_COLORS)
    
    def draw(self, screen):
        color = BALL_COLORS[self.color_index]
        
        # Draw ball with glow effect
        glow_radius = BALL_SIZE + 3
        pygame.draw.circle(screen, (color[0]//3, color[1]//3, color[2]//3), 
                          (int(self.x), int(self.y)), glow_radius)
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), BALL_SIZE)
    
    def get_rect(self):
        return pygame.Rect(self.x - BALL_SIZE, self.y - BALL_SIZE, 
                          BALL_SIZE * 2, BALL_SIZE * 2)

class AIPlayer:
    def __init__(self, paddle, difficulty=0.8):
        self.paddle = paddle
        self.difficulty = difficulty  # 0.0 to 1.0, higher is harder
        
    def update(self, ball):
        # AI follows the ball with some imperfection
        paddle_center = self.paddle.y + self.paddle.height // 2
        ball_y = ball.y
        
        # Add some randomness to make AI beatable
        if random.random() < self.difficulty:
            if ball_y < paddle_center - 10:
                self.paddle.move_up()
            elif ball_y > paddle_center + 10:
                self.paddle.move_down()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Colorful Pong Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.big_font = pygame.font.Font(None, 72)
        
        self.sound_manager = SoundManager()
        
        # Game objects
        self.player_paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, NEON_BLUE)
        self.ai_paddle = Paddle(SCREEN_WIDTH - 30 - PADDLE_WIDTH, 
                               SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, NEON_RED)
        self.ball = Ball()
        self.ai_player = AIPlayer(self.ai_paddle, difficulty=0.7)
        
        # Game state
        self.player_score = 0
        self.ai_score = 0
        self.player_name = ""
        self.game_state = "name_input"  # "name_input", "playing", "game_over"
        self.input_text = ""
        
        # Load high scores
        self.high_scores = self.load_high_scores()
    
    def load_high_scores(self):
        """Load high scores from file"""
        try:
            if os.path.exists("high_scores.json"):
                with open("high_scores.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_high_scores(self):
        """Save high scores to file"""
        try:
            with open("high_scores.json", "w") as f:
                json.dump(self.high_scores, f)
        except:
            pass
    
    def add_high_score(self, name, score):
        """Add a new high score"""
        self.high_scores.append({"name": name, "score": score})
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep top 10
        self.save_high_scores()
    
    def handle_name_input(self, event):
        """Handle name input events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    self.player_name = self.input_text.strip()
                    self.game_state = "playing"
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if len(self.input_text) < 15:  # Limit name length
                    self.input_text += event.unicode
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.game_state == "name_input":
                self.handle_name_input(event)
            elif self.game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
        
        return True
    
    def handle_input(self):
        """Handle continuous input (paddle movement)"""
        if self.game_state != "playing":
            return
            
        keys = pygame.key.get_pressed()
        mouse_y = pygame.mouse.get_pos()[1]
        
        # Keyboard controls
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_paddle.move_up()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_paddle.move_down()
        
        # Mouse controls (optional)
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            paddle_center = self.player_paddle.y + self.player_paddle.height // 2
            if mouse_y < paddle_center - 10:
                self.player_paddle.move_up()
            elif mouse_y > paddle_center + 10:
                self.player_paddle.move_down()
    
    def update_game(self):
        """Update game logic"""
        if self.game_state != "playing":
            return
        
        # Move ball
        self.ball.move()
        
        # Update AI
        self.ai_player.update(self.ball)
        
        # Ball collision with top/bottom walls
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
                self.add_high_score(self.player_name, self.player_score)
        elif self.ball.x > SCREEN_WIDTH:
            self.player_score += 1
            self.sound_manager.play('score')
            self.ball.reset()
            if self.player_score >= 10:  # Game ends at 10 points
                self.game_state = "game_over"
                self.add_high_score(self.player_name, self.player_score)
    
    def draw_background(self):
        """Draw animated background"""
        self.screen.fill(DARK_BLUE)
        
        # Draw center line
        for i in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.rect(self.screen, WHITE, 
                           (SCREEN_WIDTH // 2 - 2, i, 4, 10))
    
    def draw_name_input(self):
        """Draw name input screen"""
        self.screen.fill(DARK_BLUE)
        
        title_text = self.big_font.render("COLORFUL PONG", True, NEON_YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)
        
        prompt_text = self.font.render("Enter your name:", True, WHITE)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        self.screen.blit(prompt_text, prompt_rect)
        
        # Input box
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 300, 300, 50)
        pygame.draw.rect(self.screen, WHITE, input_box, 2)
        
        input_surface = self.font.render(self.input_text, True, WHITE)
        self.screen.blit(input_surface, (input_box.x + 10, input_box.y + 10))
        
        instruction_text = self.font.render("Press ENTER to start", True, NEON_GREEN)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
        self.screen.blit(instruction_text, instruction_rect)
    
    def draw_game(self):
        """Draw game screen"""
        self.draw_background()
        
        # Draw game objects
        self.player_paddle.draw(self.screen)
        self.ai_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw scores
        player_text = self.font.render(f"{self.player_name}: {self.player_score}", True, NEON_BLUE)
        ai_text = self.font.render(f"AI: {self.ai_score}", True, NEON_RED)
        
        self.screen.blit(player_text, (50, 30))
        ai_text_rect = ai_text.get_rect()
        ai_text_rect.topright = (SCREEN_WIDTH - 50, 30)
        self.screen.blit(ai_text, ai_text_rect)
        
        # Draw speed indicator
        speed_text = self.font.render(f"Speed: {self.ball.speed:.1f}", True, WHITE)
        speed_rect = speed_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(speed_text, speed_rect)
    
    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(DARK_BLUE)
        
        if self.player_score > self.ai_score:
            result_text = self.big_font.render("YOU WIN!", True, NEON_GREEN)
        else:
            result_text = self.big_font.render("AI WINS!", True, NEON_RED)
        
        result_rect = result_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(result_text, result_rect)
        
        score_text = self.font.render(f"Final Score - {self.player_name}: {self.player_score}, AI: {self.ai_score}", 
                                    True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 220))
        self.screen.blit(score_text, score_rect)
        
        # Draw high scores
        if self.high_scores:
            high_score_title = self.font.render("HIGH SCORES", True, NEON_YELLOW)
            title_rect = high_score_title.get_rect(center=(SCREEN_WIDTH // 2, 300))
            self.screen.blit(high_score_title, title_rect)
            
            for i, score in enumerate(self.high_scores[:5]):  # Show top 5
                score_line = f"{i+1}. {score['name']}: {score['score']}"
                score_surface = self.font.render(score_line, True, WHITE)
                score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 340 + i * 30))
                self.screen.blit(score_surface, score_rect)
        
        restart_text = self.font.render("Press SPACE to play again or ESC to quit", True, NEON_GREEN)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 520))
        self.screen.blit(restart_text, restart_rect)
    
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
            
            # Draw everything
            if self.game_state == "name_input":
                self.draw_name_input()
            elif self.game_state == "playing":
                self.draw_game()
            elif self.game_state == "game_over":
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
