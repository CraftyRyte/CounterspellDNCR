from . import entity
import pygame as pyg

class Player(entity.Entity):
    def __init__(this, position, image_path, speed_mag):
        super().__init__(position, image_path)
        this.magnitude_speed = speed_mag
    
    def update(this, dt):
        this.player_movement_logic()
        super().update(dt)
    
    def player_movement_logic(this):
        mouse_pos = pyg.mouse.get_pos()
        
        if mouse_pos == this.rect.center:
            this.velocity = pyg.math.Vector2(0, 0)

        this.rotate_towards_pos(mouse_pos)
        this.move_towards_pos(mouse_pos)