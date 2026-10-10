import time
from .ball import Ball
from .paddle import Paddle
from .tracker import GameTracker
from ..config.parameters import GameConfig, TrainingConfig

class PongGame:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.ball = Ball(GameConfig.GAME_WIDTH // 2, GameConfig.GAME_HEIGHT // 2)
        
        self.left_paddle = Paddle(30, GameConfig.GAME_HEIGHT // 2 - GameConfig.PADDLE_HEIGHT // 2, "left")
        self.right_paddle = Paddle(GameConfig.GAME_WIDTH - 30 - GameConfig.PADDLE_WIDTH, 
                                   GameConfig.GAME_HEIGHT // 2 - GameConfig.PADDLE_HEIGHT // 2, "right")
        
        self.tracker = GameTracker()
        self.game_time = 0
        self.start_time = time.time()
        self.winner = None
        self.game_over = False
        
    def reset_positions(self):
        self.ball.reset()
        self.left_paddle.reset_position()
        self.right_paddle.reset_position()
        
    def get_game_state(self):
        return {
            'ball_x': self.ball.x,
            'ball_y': self.ball.y,
            'ball_velocity_x': self.ball.velocity_x,
            'ball_velocity_y': self.ball.velocity_y,
            'left_paddle_y': self.left_paddle.y,
            'right_paddle_y': self.right_paddle.y,
            'left_score': self.left_paddle.score,
            'right_score': self.right_paddle.score,
            'hits': self.hits,
            'game_time': self.game_time
        }
    
    def get_ai_inputs(self, side):
        if side == "left":
            paddle = self.left_paddle
            is_left = 1.0
            ball_approaching = 1.0 if self.ball.velocity_x < 0 else 0.0
        else:
            paddle = self.right_paddle  
            is_left = 0.0
            ball_approaching = 1.0 if self.ball.velocity_x > 0 else 0.0
        
        return [
            paddle.y / GameConfig.GAME_HEIGHT,                                                    
            (paddle.get_center_y() - self.ball.y) / GameConfig.GAME_HEIGHT,                                 
            self.ball.x / GameConfig.GAME_WIDTH,                                                 
            self.ball.y / GameConfig.GAME_HEIGHT,                                               
            max(-10.0, min(10.0, self.ball.velocity_x)) / 10.0,                                             
            max(-10.0, min(10.0, self.ball.velocity_y)) / 10.0,                                             
            ball_approaching,                                                                             
            is_left,                                                                              
        ]
    
    def update(self, left_action, right_action):
        if self.game_over:
            return False
        
        self.game_time = time.time() - self.start_time
        
                       
        if self.game_time > TrainingConfig.GAME_TIMEOUT:
            self.game_over = True
            self.winner = self.get_current_winner()
            return False
        
        left_valid = self.left_paddle.update(left_action)
        right_valid = self.right_paddle.update(right_action)
        
        self.ball.update()
        
                                    
        if self.ball.check_collision(self.left_paddle):
            if self.ball.velocity_x < 0:                                               
                self.ball.bounce_paddle(self.left_paddle.y, self.left_paddle.height)
                self.tracker.ball_hit_by_paddle("left")
                
        if self.ball.check_collision(self.right_paddle):
            if self.ball.velocity_x > 0:                                               
                self.ball.bounce_paddle(self.right_paddle.y, self.right_paddle.height)
                self.tracker.ball_hit_by_paddle("right")
        
                                         
        if self.ball.is_out_of_bounds():
            winner = self.ball.get_winner()
            self.tracker.point_scored(winner)
            
                                              
            if winner == "left":
                self.left_paddle.score += 1
            elif winner == "right":
                self.right_paddle.score += 1
            
                                                           
            game_winner = self.tracker.get_winner(TrainingConfig.MAX_POINTS_PER_GAME)
            if game_winner:
                self.winner = game_winner
                self.game_over = True
                return False
            else:
                                                               
                self.reset_positions()
        
        return left_valid, right_valid
    
    def is_game_over(self):
        return self.game_over
    
    def get_winner(self):
        return self.winner
    
    def get_current_winner(self):
        if self.tracker.left_points > self.tracker.right_points:
            return "left"
        elif self.tracker.right_points > self.tracker.left_points:
            return "right"
        return None
    
    def get_fitness_data(self):
        return {
            'left_hits': self.tracker.left_hits,
            'right_hits': self.tracker.right_hits,
            'left_points': self.tracker.left_points,
            'right_points': self.tracker.right_points,
            'total_hits': self.tracker.total_hits,
            'game_time': self.game_time,
            'left_score': self.left_paddle.score,
            'right_score': self.right_paddle.score
        }