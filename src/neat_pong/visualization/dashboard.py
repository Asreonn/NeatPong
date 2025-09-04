import pygame
import math
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import numpy as np
from ..config.parameters import GameConfig, VisualizationConfig
from ..game.game import PongGame

class VisualizationDashboard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pygame.display.set_caption("NEAT Pong - AI Training Dashboard")
        
        self.font = pygame.font.Font(None, VisualizationConfig.FONT_SIZE)
        self.title_font = pygame.font.Font(None, VisualizationConfig.TITLE_FONT_SIZE)
        self.small_font = pygame.font.Font(None, VisualizationConfig.SMALL_FONT_SIZE)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.speed_mode = "normal"                      
        self.frame_counter = 0
        
                             
        self.current_generation = 0
        self.current_agents = []
        self.fitness_history = []
        self.current_game = None
        self.current_agent1 = None
        self.current_agent2 = None
        
                                      
        self.demo_game = PongGame()

    def draw_controls_bar(self, x_offset, y_offset, width, height):
        pygame.draw.rect(self.screen, (32, 32, 48), (x_offset, y_offset, width, height))
        pygame.draw.rect(self.screen, (60, 60, 80), (x_offset+2, y_offset+2, width-4, height-4))
        title = self.font.render("Controls", True, (255, 220, 180))
        hint = self.small_font.render("SPACE: Speed  |  ESC: Stop  |  Q: Quit", True, (220, 220, 220))
        self.screen.blit(title, (x_offset + 10, y_offset + 6))
        self.screen.blit(hint, (x_offset + 10, y_offset + 26))
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("\n⏹  Training stopped by user (ESC). Saving best model...")
                    self.running = False
                elif event.key == pygame.K_q:
                    print("\n⏹  Training stopped by user (Q). Saving best model...")
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.toggle_speed()
    
    def toggle_speed(self):
        if self.speed_mode == "normal":
            self.speed_mode = "fast"
        else:
            self.speed_mode = "normal"
    
    def draw_game(self, game, x_offset=0, y_offset=0):
                                   
        pygame.draw.rect(self.screen, GameConfig.BLACK, 
                        (x_offset, y_offset, GameConfig.GAME_WIDTH, GameConfig.GAME_HEIGHT))
        
                          
        for i in range(0, GameConfig.GAME_HEIGHT, 20):
            pygame.draw.rect(self.screen, GameConfig.WHITE,
                           (x_offset + GameConfig.GAME_WIDTH//2 - 2, y_offset + i, 4, 10))
        
                      
        pygame.draw.rect(self.screen, GameConfig.WHITE,
                        (x_offset + game.left_paddle.x, y_offset + game.left_paddle.y,
                         game.left_paddle.width, game.left_paddle.height))
        
        pygame.draw.rect(self.screen, GameConfig.WHITE,
                        (x_offset + game.right_paddle.x, y_offset + game.right_paddle.y,
                         game.right_paddle.width, game.right_paddle.height))
        
                   
        pygame.draw.circle(self.screen, GameConfig.WHITE,
                         (int(x_offset + game.ball.x), int(y_offset + game.ball.y)),
                         game.ball.size)
        
                     
        left_score = self.font.render(f"{game.left_paddle.score}", True, GameConfig.WHITE)
        right_score = self.font.render(f"{game.right_paddle.score}", True, GameConfig.WHITE)
        
        self.screen.blit(left_score, (x_offset + GameConfig.GAME_WIDTH//4, y_offset + 30))
        self.screen.blit(right_score, (x_offset + 3*GameConfig.GAME_WIDTH//4, y_offset + 30))
    
    def draw_neural_network(self, agent, x_offset, y_offset, width, height):
        if not agent:
            return
        
        network = agent.network
        genome = agent.genome
        
                                               
        pygame.draw.rect(self.screen, (30, 30, 40), (x_offset, y_offset, width, height))
        pygame.draw.rect(self.screen, (50, 50, 70), (x_offset+2, y_offset+2, width-4, height-4))
        
                                 
        title = self.title_font.render("AI Brain", True, (255, 255, 255))
        fitness_text = self.small_font.render(f"Fitness: {agent.fitness:.1f}", True, (150, 255, 150))
        self.screen.blit(title, (x_offset + 10, y_offset + 10))
        self.screen.blit(fitness_text, (x_offset + 10, y_offset + 30))
        
                               
        input_nodes = [i for i in network.input_nodes]
        output_nodes = [i for i in network.output_nodes]
        hidden_nodes = [i for i in network.node_evals if i[0] not in input_nodes and i[0] not in output_nodes]
        
                                                 
        start_y = y_offset + 60
        end_y = y_offset + height - 30
        input_y_positions = np.linspace(start_y, end_y, len(input_nodes))
        output_y_positions = np.linspace(start_y, end_y, len(output_nodes))
        
                                                
        for connection_key, connection in genome.connections.items():
            if connection.enabled:
                source_id, target_id = connection_key
                
                                           
                if source_id in input_nodes:
                    source_idx = input_nodes.index(source_id)
                    source_pos = (x_offset + 50, input_y_positions[source_idx])
                else:
                    source_pos = (x_offset + width//2, y_offset + height//2)
                
                                           
                if target_id in output_nodes:
                    target_idx = output_nodes.index(target_id)
                    target_pos = (x_offset + width - 50, output_y_positions[target_idx])
                else:
                    target_pos = (x_offset + width//2, y_offset + height//2)
                
                                             
                weight_strength = min(abs(connection.weight), 3.0) / 3.0
                if connection.weight > 0:
                    color = (int(100 + 155 * weight_strength), int(255 * weight_strength), int(100 + 155 * weight_strength))
                else:
                    color = (int(255 * weight_strength), int(100 + 155 * weight_strength), int(100 + 155 * weight_strength))
                
                thickness = max(1, int(weight_strength * 4))
                pygame.draw.line(self.screen, color, source_pos, target_pos, thickness)
        
                                      
        input_labels = ["PadY", "RelY", "BallX", "BallY", "VelX", "VelY", "Coming", "Side"]
        for i, (node_id, y_pos) in enumerate(zip(input_nodes, input_y_positions)):
                                   
            pygame.draw.circle(self.screen, (70, 130, 255), (x_offset + 50, int(y_pos)), VisualizationConfig.NETWORK_NODE_SIZE + 2)
            pygame.draw.circle(self.screen, (100, 160, 255), (x_offset + 50, int(y_pos)), VisualizationConfig.NETWORK_NODE_SIZE)
            
                                            
            if i < len(input_labels):
                label = self.small_font.render(input_labels[i], True, (200, 200, 255))
                self.screen.blit(label, (x_offset + 75, int(y_pos) - 6))
        
                                                 
        output_labels = ["Stay", "Up", "Down"]
        output_colors = [(180, 180, 180), (100, 255, 100), (255, 100, 100)]
        for i, (node_id, y_pos) in enumerate(zip(output_nodes, output_y_positions)):
            color = output_colors[i] if i < len(output_colors) else (150, 150, 150)
            
                            
            pygame.draw.circle(self.screen, tuple(min(255, c+30) for c in color), (x_offset + width - 50, int(y_pos)), VisualizationConfig.NETWORK_NODE_SIZE + 2)
            pygame.draw.circle(self.screen, color, (x_offset + width - 50, int(y_pos)), VisualizationConfig.NETWORK_NODE_SIZE)
            
                    
            if i < len(output_labels):
                label = self.small_font.render(output_labels[i], True, color)
                label_rect = label.get_rect()
                self.screen.blit(label, (x_offset + width - 120, int(y_pos) - 6))
        
                                  
        if hidden_nodes:
            pygame.draw.circle(self.screen, (200, 200, 100), (x_offset + width//2, y_offset + height//2), VisualizationConfig.NETWORK_NODE_SIZE + 1)
            pygame.draw.circle(self.screen, (255, 255, 150), (x_offset + width//2, y_offset + height//2), VisualizationConfig.NETWORK_NODE_SIZE)
            
            hidden_label = self.small_font.render("Hidden", True, (255, 255, 200))
            self.screen.blit(hidden_label, (x_offset + width//2 + 20, y_offset + height//2 - 6))
    
    def draw_fitness_graph(self, x_offset, y_offset, width, height):
        if not self.fitness_history:
            return
        
                          
        pygame.draw.rect(self.screen, GameConfig.DARK_GRAY, (x_offset, y_offset, width, height))
        
               
        title = self.font.render("Fitness Evolution", True, GameConfig.WHITE)
        self.screen.blit(title, (x_offset + 10, y_offset + 10))
        
        if len(self.fitness_history) < 2:
            return
        
                  
        generations = [entry['generation'] for entry in self.fitness_history[-VisualizationConfig.GRAPH_HISTORY_SIZE:]]
        best_fitness = [entry['best_fitness'] for entry in self.fitness_history[-VisualizationConfig.GRAPH_HISTORY_SIZE:]]
        avg_fitness = [entry['avg_fitness'] for entry in self.fitness_history[-VisualizationConfig.GRAPH_HISTORY_SIZE:]]
        
                           
        min_gen = min(generations)
        max_gen = max(generations)
        min_fitness = min(min(best_fitness), min(avg_fitness))
        max_fitness = max(max(best_fitness), max(avg_fitness))
        
        if max_fitness == min_fitness:
            max_fitness = min_fitness + 1
        
        graph_x = x_offset + 50
        graph_y = y_offset + 40
        graph_width = width - 100
        graph_height = height - 80
        
                   
        pygame.draw.line(self.screen, GameConfig.WHITE, 
                        (graph_x, graph_y + graph_height), (graph_x + graph_width, graph_y + graph_height))
        pygame.draw.line(self.screen, GameConfig.WHITE, 
                        (graph_x, graph_y), (graph_x, graph_y + graph_height))
        
                    
        prev_best_point = None
        prev_avg_point = None
        
        for i, (gen, best, avg) in enumerate(zip(generations, best_fitness, avg_fitness)):
            x = graph_x + (gen - min_gen) / max(1, max_gen - min_gen) * graph_width
            y_best = graph_y + graph_height - (best - min_fitness) / (max_fitness - min_fitness) * graph_height
            y_avg = graph_y + graph_height - (avg - min_fitness) / (max_fitness - min_fitness) * graph_height
            
            current_best_point = (int(x), int(y_best))
            current_avg_point = (int(x), int(y_avg))
            
            if prev_best_point:
                pygame.draw.line(self.screen, GameConfig.GREEN, prev_best_point, current_best_point, 2)
            if prev_avg_point:
                pygame.draw.line(self.screen, GameConfig.BLUE, prev_avg_point, current_avg_point, 2)
            
            prev_best_point = current_best_point
            prev_avg_point = current_avg_point
        
                
        legend_y = y_offset + height - 25
        pygame.draw.line(self.screen, GameConfig.GREEN, (x_offset + 10, legend_y), (x_offset + 30, legend_y), 3)
        best_label = self.font.render("Best", True, GameConfig.WHITE)
        self.screen.blit(best_label, (x_offset + 35, legend_y - 8))
        
        pygame.draw.line(self.screen, GameConfig.BLUE, (x_offset + 80, legend_y), (x_offset + 100, legend_y), 3)
        avg_label = self.font.render("Average", True, GameConfig.WHITE)
        self.screen.blit(avg_label, (x_offset + 105, legend_y - 8))
    
    def draw_stats(self, x_offset, y_offset, width, height):
                                               
        pygame.draw.rect(self.screen, (25, 25, 35), (x_offset, y_offset, width, height))
        pygame.draw.rect(self.screen, (40, 40, 55), (x_offset+2, y_offset+2, width-4, height-4))
        
               
        title = self.title_font.render("Training Stats", True, (255, 255, 255))
        self.screen.blit(title, (x_offset + 10, y_offset + 10))
        
        y_pos = y_offset + 40
        line_height = 22
        
                                             
        gen_text = self.font.render(f"Generation: {self.current_generation}", True, (150, 255, 150))
        self.screen.blit(gen_text, (x_offset + 10, y_pos))
        y_pos += line_height
        
                                      
        speed_color = (255, 100, 100) if self.speed_mode == "fast" else (100, 200, 255)
        speed_text = self.font.render(f"Speed: {self.speed_mode.upper()}", True, speed_color)
        self.screen.blit(speed_text, (x_offset + 10, y_pos))
        
                         
        if self.speed_mode == "fast":
            speed_info = f"({VisualizationConfig.TRAINING_SPEED_MULTIPLIER}x Speed)"
        else:
            speed_info = f"({VisualizationConfig.FPS_NORMAL} FPS)"
        fps_text = self.small_font.render(speed_info, True, speed_color)
        self.screen.blit(fps_text, (x_offset + 120, y_pos + 3))
        y_pos += line_height
        
                          
        if self.current_agents:
            agents_text = self.font.render(f"Population: {len(self.current_agents)}", True, (200, 200, 255))
            self.screen.blit(agents_text, (x_offset + 10, y_pos))
            y_pos += line_height
            
                                                 
            if self.fitness_history:
                latest = self.fitness_history[-1]
                
                                                
                best_fitness = latest['best_fitness']
                best_text = self.font.render(f"Best: {best_fitness:.1f}", True, (100, 255, 100))
                self.screen.blit(best_text, (x_offset + 10, y_pos))
                
                                                    
                bar_width = 100
                bar_height = 8
                bar_x = x_offset + width - bar_width - 10
                bar_y = y_pos + 8
                
                pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                progress_width = min(bar_width, int((best_fitness / 5000) * bar_width))
                pygame.draw.rect(self.screen, (100, 255, 100), (bar_x, bar_y, progress_width, bar_height))
                
                y_pos += line_height
                
                                 
                avg_fitness = latest['avg_fitness']
                avg_text = self.font.render(f"Avg: {avg_fitness:.1f}", True, (150, 150, 255))
                self.screen.blit(avg_text, (x_offset + 10, y_pos))
                y_pos += line_height
                
                                                     
                if len(self.fitness_history) > 1:
                    latest_entry = self.fitness_history[-1]
                    
                                             
                    if latest_entry.get('improvement_made', False):
                        imp_text = self.small_font.render("🎉 NEW BEST!", True, (100, 255, 100))
                    else:
                        stagnation = latest_entry.get('stagnation_generations', 0)
                        if stagnation > 0:
                            imp_text = self.small_font.render(f"Stagnant: {stagnation} gens", True, (255, 200, 100))
                        else:
                            imp_text = self.small_font.render("→ No change", True, (200, 200, 200))
                    
                    self.screen.blit(imp_text, (x_offset + 10, y_pos))
                    y_pos += line_height
                    
                                                     
                    if 'stagnation_generations' in latest_entry:
                        stag_gens = latest_entry['stagnation_generations']
                        if stag_gens > 20:                                
                            warning_color = (255, 150, 100) if stag_gens < 40 else (255, 100, 100)
                            warning_text = self.small_font.render(f"⚠ {stag_gens} gens without improvement", True, warning_color)
                            self.screen.blit(warning_text, (x_offset + 10, y_pos))
                            y_pos += 18
        
                                     
        y_pos += 10
        perf_title = self.font.render("Performance:", True, (255, 255, 150))
        self.screen.blit(perf_title, (x_offset + 10, y_pos))
        y_pos += line_height
        
                                       
        frame_text = self.small_font.render(f"Frames: {self.frame_counter}", True, (200, 200, 200))
        self.screen.blit(frame_text, (x_offset + 10, y_pos))
        y_pos += 18
        
        if self.speed_mode == "fast":
            render_text = self.small_font.render(f"Training: {VisualizationConfig.TRAINING_SPEED_MULTIPLIER}x faster", True, (200, 200, 200))
            self.screen.blit(render_text, (x_offset + 10, y_pos))
            y_pos += 18
        
                          
        # Controls are now rendered in a dedicated top bar
    
    def update_visualization(self, generation, agents, fitness_history):
        self.current_generation = generation
        self.current_agents = agents
        self.fitness_history = fitness_history
        
                                                        
        if agents and len(agents) >= 2:
                                           
            sorted_agents = sorted(agents, key=lambda a: a.fitness, reverse=True)
            self.current_agent1 = sorted_agents[0]
            self.current_agent2 = sorted_agents[1] if len(sorted_agents) > 1 else sorted_agents[0]
    
    def render_frame(self):
        self.screen.fill(GameConfig.GRAY)
        
                   
        self.draw_game(self.demo_game, 0, 0)
        
                 
        sidebar_x = GameConfig.GAME_WIDTH
        
                                      
        controls_height = 44
        self.draw_controls_bar(sidebar_x, 0, GameConfig.SIDEBAR_WIDTH, controls_height)

        network_height = 200
        if self.current_agent1:
            self.draw_neural_network(self.current_agent1, sidebar_x, controls_height, GameConfig.SIDEBAR_WIDTH, network_height)
        
                       
        graph_height = 150
        self.draw_fitness_graph(sidebar_x, controls_height + network_height, GameConfig.SIDEBAR_WIDTH, graph_height)
        
                    
        stats_height = GameConfig.SCREEN_HEIGHT - (controls_height + network_height + graph_height)
        self.draw_stats(sidebar_x, controls_height + network_height + graph_height, GameConfig.SIDEBAR_WIDTH, stats_height)
        
        pygame.display.flip()
    
    def run_frame(self):
        self.handle_events()
        self.frame_counter += 1
        
                                                                           
        update_count = 1
        if self.speed_mode == "fast":
            update_count = VisualizationConfig.TRAINING_SPEED_MULTIPLIER
        
        for _ in range(update_count):
            if self.current_agent1 and self.current_agent2 and not self.demo_game.is_game_over():
                left_inputs = self.demo_game.get_ai_inputs("left")
                right_inputs = self.demo_game.get_ai_inputs("right")
                
                left_action = self.current_agent1.get_action(left_inputs)
                right_action = self.current_agent2.get_action(right_inputs)
                
                self.demo_game.update(left_action, right_action)
            elif self.demo_game.is_game_over():
                self.demo_game.reset()
        
                                                                               
        self.render_frame()
        
                                                       
        self.clock.tick(VisualizationConfig.FPS_NORMAL)
        
        return self.running
