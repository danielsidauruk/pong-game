import pygame
from constants import SCREEN_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED

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
