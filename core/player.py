from . import entity
import pygame as pyg

class Player(entity.Entity):
    def __init__(self, position, image_path, speed_mag):
        super().__init__(position, image_path)
        self.magnitude_speed = speed_mag
    
    def update(self, dt):
        self.player_movement_logic()
        super().update(dt)
    
    def player_movement_logic(self):
        mouse_pos = pyg.mouse.get_pos()
        
        if mouse_pos == self.rect.center:
            self.velocity = pyg.math.Vector2(0, 0)

        self.rotate_towards_pos(mouse_pos)
        self.move_towards_pos(mouse_pos)