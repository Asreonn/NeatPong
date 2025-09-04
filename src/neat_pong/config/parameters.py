class GameConfig:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600
    GAME_WIDTH = 800
    GAME_HEIGHT = 600
    SIDEBAR_WIDTH = 400
    
    BALL_SIZE = 10
    BALL_SPEED = 5
    PADDLE_WIDTH = 10
    PADDLE_HEIGHT = 60
    PADDLE_SPEED = 4
    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (64, 64, 64)

class TrainingConfig:
    GENERATIONS = 50
    POPULATION_SIZE = 50
    MAX_POINTS_PER_GAME = 5
    GAME_TIMEOUT = 45.0
    CHECKPOINT_INTERVAL = 5
    
                                   
    FITNESS_HIT_REWARD = 15
    FITNESS_POINT_WIN_REWARD = 100
    FITNESS_POINT_LOSS_PENALTY = -80
    FITNESS_GAME_WIN_REWARD = 200
    FITNESS_DURATION_MULTIPLIER = 2
    FITNESS_MAX_TIME_BONUS = 50
    FITNESS_INVALID_MOVE_PENALTY = -10
                                                   
    FITNESS_MOVEMENT_BONUS = 0.01                               
    FITNESS_BALL_FOLLOW_BONUS = 0.05                                  
                                                               

class VisualizationConfig:
    FPS_NORMAL = 60
    FPS_FAST = 60                                                         
    TRAINING_SPEED_MULTIPLIER = 10                                                     
    SHOW_NEURAL_NETWORK = True
    SHOW_FITNESS_GRAPH = True
    GRAPH_HISTORY_SIZE = 100
    
    NETWORK_NODE_SIZE = 15
    NETWORK_CONNECTION_WIDTH = 2
    FONT_SIZE = 14
    TITLE_FONT_SIZE = 16
    SMALL_FONT_SIZE = 12