import time
from ..config.parameters import VisualizationConfig

class SpeedController:
    def __init__(self):
        self.mode = "normal"                      
        self.last_frame_time = time.time()
        self.target_fps = VisualizationConfig.FPS_NORMAL
        
    def set_mode(self, mode):
        self.mode = mode
        if mode == "normal":
            self.target_fps = VisualizationConfig.FPS_NORMAL
        elif mode == "fast":
            self.target_fps = VisualizationConfig.FPS_FAST
    
    def toggle_mode(self):
        if self.mode == "normal":
            self.set_mode("fast")
        else:
            self.set_mode("normal")
    
    def limit_fps(self):
        if self.mode == "normal":
            current_time = time.time()
            frame_time = current_time - self.last_frame_time
            target_frame_time = 1.0 / self.target_fps
            
            if frame_time < target_frame_time:
                time.sleep(target_frame_time - frame_time)
            
            self.last_frame_time = time.time()
    
    def should_render_frame(self):
                                                                               
        if self.mode == "fast":
            current_time = time.time()
                                                
            return current_time - self.last_frame_time > 0.1
        return True
    
    def get_mode(self):
        return self.mode
    
    def get_fps(self):
        return self.target_fps