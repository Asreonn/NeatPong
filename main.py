#!/usr/bin/env python3
import argparse
import os
import sys
import threading
import time

                                  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from neat_pong.training.trainer import NEATTrainer
from neat_pong.visualization.dashboard import VisualizationDashboard
from neat_pong.config.parameters import TrainingConfig
from neat_pong.game.game import PongGame
from neat_pong.training.agent import PongAgent
import neat

class NEATPongApp:
    def __init__(self):
        self.config_path = "src/neat_pong/config/config.txt"
        self.trainer = None
        self.dashboard = None
        self.training_thread = None
        self.training_active = False
        
    def setup_trainer(self, checkpoint_path=None):
        self.trainer = NEATTrainer(self.config_path, checkpoint_path)
        
    def setup_visualization(self):
        self.dashboard = VisualizationDashboard()
        if self.trainer:
            self.trainer.set_visualization_callback(self.dashboard.update_visualization)
    
    def train_with_visualization(self, generations, show_training):
        def training_worker():
            self.training_active = True
            try:
                print(f"🚀 Starting NEAT training (Population: 1000)...")
                print("📊 Training will run continuously until you stop it")
                print("🎮 Controls:")
                print("   SPACE - Toggle normal/fast speed")
                print("   ESC/Q - Stop training and save best model")
                print("⚡ No early stopping - train as long as you want!")
                
                winner = self.trainer.train(10000)                    
                print(f"\\nTraining completed! Best genome fitness: {winner.fitness}")
                
            except Exception as e:
                print(f"Training error: {e}")
            finally:
                self.training_active = False
        
        if show_training:
            self.setup_visualization()
            self.training_thread = threading.Thread(target=training_worker, daemon=True)
            self.training_thread.start()
            
                                         
            while self.dashboard.running and self.training_active:
                if not self.dashboard.run_frame():
                    break
            
            print("\\nVisualization stopped.")
        else:
                                         
            training_worker()
    
    def train_mode(self, args):
        print("=== NEAT Pong Training Mode ===")
        self.setup_trainer()
        self.train_with_visualization(10000, args.show_training)                                        
    
    def continue_mode(self, args):
        print(f"=== NEAT Pong Continue Training Mode ===")
        if not os.path.exists(args.checkpoint):
            print(f"Error: Checkpoint file '{args.checkpoint}' not found!")
            self.list_available_checkpoints()
            return
        
        print(f"📂 Loading checkpoint: {args.checkpoint}")
        self.setup_trainer(args.checkpoint)
        self.train_with_visualization(10000, args.show_training)                                        
    
    def list_available_checkpoints(self):
        print("\n📋 Available checkpoints:")
        checkpoint_dir = "checkpoints"
        if os.path.exists(checkpoint_dir):
            checkpoints = [f for f in os.listdir(checkpoint_dir) if f.startswith("neat-checkpoint-")]
            if checkpoints:
                checkpoints.sort(key=lambda x: int(x.split("-")[-1]))
                for cp in checkpoints:
                    full_path = os.path.join(checkpoint_dir, cp)
                    print(f"   - {full_path}")
                print(f"\nUsage: python main.py --mode continue --checkpoint {os.path.join(checkpoint_dir, checkpoints[-1])}")
            else:
                print("   No checkpoints found in checkpoints/ directory")
        else:
            print("   checkpoints/ directory not found")
    
    def test_mode(self, args):
        print("=== NEAT Pong Test Mode ===")
        
        model_path = args.model or "models/best_genome.pickle"
        if not os.path.exists(model_path):
            print(f"Error: Model file '{model_path}' not found!")
            print("Train a model first using: python main.py --mode train")
            return
        
                            
        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            self.config_path
        )
        
                             
        import pickle
        with open(model_path, "rb") as f:
            genome = pickle.load(f)
        
        print(f"Loaded model with fitness: {genome.fitness}")
        
                                                                  
        agent1 = PongAgent(genome, config)
        agent2 = PongAgent(genome, config)                      
        
                                      
        self.dashboard = VisualizationDashboard()
        self.dashboard.current_generation = "DEMO"
        self.dashboard.current_agent1 = agent1
        self.dashboard.current_agent2 = agent2
        
        print("Running AI vs AI demonstration...")
        print("Press SPACE to toggle speed, ESC to exit")
        
        game = PongGame()
        games_played = 0
        
        while self.dashboard.running:
            if not self.dashboard.run_frame():
                break
            
            if not game.is_game_over():
                               
                left_inputs = game.get_ai_inputs("left")
                right_inputs = game.get_ai_inputs("right")
                
                                     
                left_action = agent1.get_action(left_inputs)
                right_action = agent2.get_action(right_inputs)
                
                             
                game.update(left_action, right_action)
                
                                              
                self.dashboard.demo_game = game
            else:
                games_played += 1
                print(f"Game {games_played} finished - Winner: {game.get_winner() or 'Tie'}")
                time.sleep(2)                             
                game.reset()
    
    def benchmark_mode(self, args):
        print("=== NEAT Pong Benchmark Mode ===")
        
        model_path = args.model or "models/best_genome.pickle"
        if not os.path.exists(model_path):
            print(f"Error: Model file '{model_path}' not found!")
            return
        
                    
        config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            self.config_path
        )
        
        import pickle
        with open(model_path, "rb") as f:
            genome = pickle.load(f)
        
        agent1 = PongAgent(genome, config)
        agent2 = PongAgent(genome, config)
        
        print(f"Running {args.benchmark_games} benchmark games...")
        
        wins_agent1 = 0
        wins_agent2 = 0
        ties = 0
        total_hits = 0
        
        for game_num in range(args.benchmark_games):
            game = PongGame()
            
            while not game.is_game_over():
                left_inputs = game.get_ai_inputs("left")
                right_inputs = game.get_ai_inputs("right")
                
                left_action = agent1.get_action(left_inputs)
                right_action = agent2.get_action(right_inputs)
                
                game.update(left_action, right_action)
            
            winner = game.get_winner()
            if winner == "left":
                wins_agent1 += 1
            elif winner == "right":
                wins_agent2 += 1
            else:
                ties += 1
            
            total_hits += game.hits
            
            if (game_num + 1) % 10 == 0:
                print(f"Completed {game_num + 1}/{args.benchmark_games} games")
        
        print("\\n=== Benchmark Results ===")
        print(f"Total games: {args.benchmark_games}")
        print(f"Agent 1 wins: {wins_agent1} ({wins_agent1/args.benchmark_games*100:.1f}%)")
        print(f"Agent 2 wins: {wins_agent2} ({wins_agent2/args.benchmark_games*100:.1f}%)")
        print(f"Ties: {ties} ({ties/args.benchmark_games*100:.1f}%)")
        print(f"Average hits per game: {total_hits/args.benchmark_games:.1f}")

def main():
    parser = argparse.ArgumentParser(description="NEAT Pong - AI Training and Testing")
    parser.add_argument("--mode", choices=["train", "test", "continue", "benchmark"], 
                       required=True, help="Mode to run the application")
    
                                                           
    parser.add_argument("--show-training", action="store_true",
                       help="Show training visualization")
    
                                 
    parser.add_argument("--checkpoint", type=str,
                       help="Checkpoint file to continue training from")
    
                              
    parser.add_argument("--model", type=str,
                       help="Model file to test (default: models/best_genome.pickle)")
    parser.add_argument("--benchmark-games", type=int, default=100,
                       help="Number of games for benchmark mode")
    
    args = parser.parse_args()
    
                                                              
    
    app = NEATPongApp()
    
    try:
        if args.mode == "train":
            app.train_mode(args)
        elif args.mode == "continue":
            if not args.checkpoint:
                print("Error: --checkpoint required for continue mode")
                sys.exit(1)
            app.continue_mode(args)
        elif args.mode == "test":
            app.test_mode(args)
        elif args.mode == "benchmark":
            app.benchmark_mode(args)
    except KeyboardInterrupt:
        print("\\nApplication interrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()