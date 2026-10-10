import neat
from ..config.parameters import TrainingConfig

class PongAgent:
    def __init__(self, genome, config):
        self.genome = genome
        self.network = neat.nn.FeedForwardNetwork.create(genome, config)
        self.fitness = 0
        self.hits = 0
        self.games_played = 0
        self.wins = 0
        self.total_game_time = 0
        self.invalid_moves = 0
        
    def get_action(self, inputs):
        output = self.network.activate(inputs)
        return output.index(max(output))                                      
    
    def add_fitness(self, reward):
        self.fitness += reward
        self.genome.fitness = self.fitness
    
    def record_hit(self):
        self.hits += 1
        self.add_fitness(TrainingConfig.FITNESS_HIT_REWARD)
    
    def record_point_won(self):
        self.add_fitness(TrainingConfig.FITNESS_POINT_WIN_REWARD)
    
    def record_point_lost(self):
        self.add_fitness(TrainingConfig.FITNESS_POINT_LOSS_PENALTY)
    
    def record_win(self):
        self.wins += 1
        self.add_fitness(TrainingConfig.FITNESS_GAME_WIN_REWARD)
    
    def record_game_time(self, game_time):
        self.total_game_time += game_time
        time_bonus = min(game_time * TrainingConfig.FITNESS_DURATION_MULTIPLIER, TrainingConfig.FITNESS_MAX_TIME_BONUS)
        self.add_fitness(time_bonus)
    
    def record_invalid_move(self):
        self.invalid_moves += 1
        self.add_fitness(TrainingConfig.FITNESS_INVALID_MOVE_PENALTY)
    
    def record_movement_bonus(self):
        self.add_fitness(TrainingConfig.FITNESS_MOVEMENT_BONUS)
    
    def record_staying_penalty(self):
        self.add_fitness(TrainingConfig.FITNESS_STAYING_PENALTY)
    
    def record_ball_follow_bonus(self):
        self.add_fitness(TrainingConfig.FITNESS_BALL_FOLLOW_BONUS)
    
    def finish_game(self):
        self.games_played += 1
    
    def get_stats(self):
        return {
            'fitness': self.fitness,
            'hits': self.hits,
            'games_played': self.games_played,
            'wins': self.wins,
            'avg_game_time': self.total_game_time / max(1, self.games_played),
            'invalid_moves': self.invalid_moves,
            'win_rate': self.wins / max(1, self.games_played)
        }