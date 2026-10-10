import math
import random
from ..config.parameters import GameConfig

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = GameConfig.BALL_SIZE
        self.speed = GameConfig.BALL_SPEED
        self.reset()
    
    def reset(self):
        self.x = GameConfig.GAME_WIDTH // 2
        self.y = GameConfig.GAME_HEIGHT // 2
        
        angle = random.choice([
            random.uniform(-math.pi/4, math.pi/4),
            random.uniform(3*math.pi/4, 5*math.pi/4)
        ])
        
        self.velocity_x = self.speed * math.cos(angle)
        self.velocity_y = self.speed * math.sin(angle)
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        if self.y <= self.size or self.y >= GameConfig.GAME_HEIGHT - self.size:
            self.velocity_y = -self.velocity_y
            self.y = max(self.size, min(GameConfig.GAME_HEIGHT - self.size, self.y))
    
    def bounce_paddle(self, paddle_y, paddle_height):
        relative_intersect_y = (paddle_y + paddle_height/2) - self.y
        normalized_intersect_y = relative_intersect_y / (paddle_height/2)
        bounce_angle = normalized_intersect_y * math.pi/4
        
        direction = 1 if self.velocity_x < 0 else -1
        self.velocity_x = direction * self.speed * math.cos(bounce_angle)
        self.velocity_y = self.speed * -math.sin(bounce_angle)
        
        self.speed = min(self.speed * 1.05, GameConfig.BALL_SPEED * 2)
    
    def check_collision(self, paddle):
        return (self.x - self.size < paddle.x + paddle.width and 
                self.x + self.size > paddle.x and
                self.y - self.size < paddle.y + paddle.height and
                self.y + self.size > paddle.y)
    
    def is_out_of_bounds(self):
        return self.x < 0 or self.x > GameConfig.GAME_WIDTH
    
    def get_winner(self):
        if self.x < 0:
            return "right"
        elif self.x > GameConfig.GAME_WIDTH:
            return "left"
        return None