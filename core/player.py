from . import entity
import pygame as pyg

class Player(entity.Entity):
    def __init__(self, position, image_path, speed_mag):
        super().__init__(position, image_path)
        self.magnitude_speed = speed_mag
    
    def update(self, dt):
        self.player_movement_logic()
        super().update(dt)
    
    def rotate_towards_mouse(self, mouse_pos):
        angles = self.determine_rotation_angles(mouse_pos, self.rect.center)
        self.rotate(angles)
    
    def move_player_towards_mouse(self, mouse_pos):
        mousex, mousey = mouse_pos

        direction = pyg.math.Vector2(mousex - self.position.x, mousey - self.position.y).normalize()

        self.velocity = direction * self.magnitude_speed
    
    def player_movement_logic(self):
        mouse_pos = pyg.mouse.get_pos()
        
        if mouse_pos == self.rect.center:
            self.velocity = pyg.math.Vector2(0, 0)

        self.rotate_towards_mouse(mouse_pos)
        self.move_player_towards_mouse(mouse_pos)