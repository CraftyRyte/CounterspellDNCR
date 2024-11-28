from . import entity
import pygame as pyg

class Henchman(entity.Entity):
    def __init__(this, position, image_path, speed_magnitude, *groups):
        super().__init__(position, image_path, speed_magnitude, *groups)
        
    def update(this, dt, player_center):
        this.move_henchman_logic(player_center)
        super().update(dt)

    def move_henchman_logic(this, player_center):
        this.rotate_towards_pos(player_center)
        this.move_towards_pos(player_center)
        return