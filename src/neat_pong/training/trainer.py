import neat
import pickle
import random
import os
from .agent import PongAgent
from ..game.game import PongGame
from ..config.parameters import TrainingConfig

class NEATTrainer:
    def __init__(self, config_path, checkpoint_path=None):
        self.config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )
        # Ensure output directories exist
        os.makedirs("checkpoints", exist_ok=True)
        
        if checkpoint_path:
            self.population = neat.Checkpointer.restore_checkpoint(checkpoint_path)
        else:
            self.population = neat.Population(self.config)
        
        self.population.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.population.add_reporter(self.stats)
        self.population.add_reporter(neat.Checkpointer(TrainingConfig.CHECKPOINT_INTERVAL, filename_prefix='checkpoints/neat-checkpoint-'))
        
        self.generation = 0
        self.best_genome = None
        self.fitness_history = []
        self.visualization_callback = None
        self.last_improvement_generation = 0
        self.stagnation_threshold = 50                                            
        self.continuous_training = True
    
    def set_visualization_callback(self, callback):
        self.visualization_callback = callback
    
    def evaluate_genome_pair(self, genome1, genome2):
        agent1 = PongAgent(genome1, self.config)
        agent2 = PongAgent(genome2, self.config)
        
        total_fitness1 = 0
        total_fitness2 = 0
        
                                                        
        games_per_match = 3
        
        for _ in range(games_per_match):
            game = PongGame()
            
            while not game.is_game_over():
                                              
                left_inputs = game.get_ai_inputs("left")
                right_inputs = game.get_ai_inputs("right")
                
                                         
                left_action = agent1.get_action(left_inputs)
                right_action = agent2.get_action(right_inputs)
                
                             
                result = game.update(left_action, right_action)
                
                                                    
                if isinstance(result, tuple):
                    if not result[0]:
                        agent1.record_invalid_move()
                    else:
                                             
                        if left_action != 0:          
                            agent1.record_movement_bonus()
                                                         
                            paddle_center = game.left_paddle.get_center_y()
                            if ((left_action == 1 and game.ball.y < paddle_center) or 
                                (left_action == 2 and game.ball.y > paddle_center)):
                                agent1.record_ball_follow_bonus()
                                                                         
                    
                    if not result[1]:
                        agent2.record_invalid_move()
                    else:
                                               
                        if right_action != 0:          
                            agent2.record_movement_bonus()
                                                         
                            paddle_center = game.right_paddle.get_center_y()
                            if ((right_action == 1 and game.ball.y < paddle_center) or 
                                (right_action == 2 and game.ball.y > paddle_center)):
                                agent2.record_ball_follow_bonus()
                                                                         
            
                                                      
            fitness_data = game.get_fitness_data()
            winner = game.get_winner()
            
                                                              
            for _ in range(fitness_data['left_hits']):
                agent1.record_hit()
            for _ in range(fitness_data['right_hits']):
                agent2.record_hit()
            
                                               
            for _ in range(fitness_data['left_points']):
                agent1.record_point_won()
                agent2.record_point_lost()
            for _ in range(fitness_data['right_points']):
                agent2.record_point_won()
                agent1.record_point_lost()
            
                                   
            agent1.record_game_time(fitness_data['game_time'])
            agent2.record_game_time(fitness_data['game_time'])
            
                                  
            if winner == "left":
                agent1.record_win()
            elif winner == "right":
                agent2.record_win()
            
            agent1.finish_game()
            agent2.finish_game()
            
            total_fitness1 += agent1.fitness
            total_fitness2 += agent2.fitness
        
                           
        genome1.fitness = total_fitness1 / games_per_match
        genome2.fitness = total_fitness2 / games_per_match
        
        return agent1, agent2
    
    def evaluate_population(self, genomes, config):
        self.generation += 1
        
                                                     
        genome_list = list(genomes)
        agents = []
        
                                   
        for i in range(0, len(genome_list) - 1, 2):
            genome_id1, genome1 = genome_list[i]
            genome_id2, genome2 = genome_list[i + 1]
            
            agent1, agent2 = self.evaluate_genome_pair(genome1, genome2)
            agents.extend([agent1, agent2])
        
                           
        if len(genome_list) % 2 == 1:
            genome_id, genome = genome_list[-1]
                                                   
            if len(genome_list) > 1:
                random_idx = random.randint(0, len(genome_list) - 2)
                _, random_genome = genome_list[random_idx]
                agent1, _ = self.evaluate_genome_pair(genome, random_genome)
                agents.append(agent1)
            else:
                                                       
                genome.fitness = 0
        
                                                
        best_fitness = max(genome.fitness for _, genome in genomes)
        generation_best = None
        for _, genome in genomes:
            if genome.fitness == best_fitness:
                generation_best = genome
                break
        
        improvement_made = False
        if self.best_genome is None or best_fitness > self.best_genome.fitness:
            self.best_genome = generation_best
            self.last_improvement_generation = self.generation
            improvement_made = True
        
                                
        avg_fitness = sum(genome.fitness for _, genome in genomes) / len(genomes)
        stagnation_generations = self.generation - self.last_improvement_generation
        
        self.fitness_history.append({
            'generation': self.generation,
            'best_fitness': best_fitness,
            'avg_fitness': avg_fitness,
            'improvement_made': improvement_made,
            'stagnation_generations': stagnation_generations
        })
        
                                            
        if self.visualization_callback:
            self.visualization_callback(self.generation, agents, self.fitness_history)
        
                                     
        status_msg = f"Generation {self.generation}: Best={best_fitness:.2f}, Avg={avg_fitness:.2f}"
        if improvement_made:
            status_msg += " 🎉 NEW BEST!"
        elif stagnation_generations > 0:
            status_msg += f" (Stagnant: {stagnation_generations} gens)"
        
        print(status_msg)
    
    def train(self, generations=None):
        if generations is None:
            generations = TrainingConfig.GENERATIONS
        
        winner = self.population.run(self.evaluate_population, generations)
        
                              
        os.makedirs("models", exist_ok=True)
        with open("models/best_genome.pickle", "wb") as f:
            pickle.dump(winner, f)
        
        return winner
    
    def load_best_genome(self, path="models/best_genome.pickle"):
        with open(path, "rb") as f:
            return pickle.load(f)
