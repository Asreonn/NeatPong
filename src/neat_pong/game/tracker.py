class GameTracker:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.left_hits = 0
        self.right_hits = 0
        self.left_points = 0  
        self.right_points = 0
        self.total_hits = 0
        self.game_duration = 0
        
    def ball_hit_by_paddle(self, side):
        self.total_hits += 1
        if side == "left":
            self.left_hits += 1
            return "left"
        else:
            self.right_hits += 1 
            return "right"
    
    def point_scored(self, winner):
        if winner == "left":
            self.left_points += 1
        elif winner == "right":
            self.right_points += 1
    
    def get_total_points(self):
        return self.left_points + self.right_points
    
    def get_winner(self, max_points=5):
        if self.left_points >= max_points:
            return "left"
        elif self.right_points >= max_points:
            return "right"
        return None
    
    def get_stats(self):
        return {
            'left_hits': self.left_hits,
            'right_hits': self.right_hits,
            'left_points': self.left_points,
            'right_points': self.right_points,
            'total_hits': self.total_hits,
            'total_points': self.get_total_points()
        }