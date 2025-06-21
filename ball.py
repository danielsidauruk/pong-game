import pygame
import random
import math
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, BALL_SIZE, INITIAL_BALL_SPEED, 
                      SPEED_INCREMENT, MAX_BALL_SPEED, BALL_COLORS)

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
