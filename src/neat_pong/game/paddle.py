from ..config.parameters import GameConfig

class Paddle:
    def __init__(self, x, y, side="left"):
        self.x = x
        self.y = y
        self.width = GameConfig.PADDLE_WIDTH
        self.height = GameConfig.PADDLE_HEIGHT
        self.speed = GameConfig.PADDLE_SPEED
        self.side = side
        self.score = 0
        
    def update(self, action):
        if action == 0:              
            return True
        elif action == 1:           
            if self.y > 0:
                self.y = max(0, self.y - self.speed)
                return True
            return False                
        elif action == 2:             
            if self.y + self.height < GameConfig.GAME_HEIGHT:
                self.y = min(GameConfig.GAME_HEIGHT - self.height, self.y + self.speed)
                return True
            return False                
        return False
    
    def get_center_y(self):
        return self.y + self.height // 2
    
    def reset_position(self):
        self.y = GameConfig.GAME_HEIGHT // 2 - self.height // 2