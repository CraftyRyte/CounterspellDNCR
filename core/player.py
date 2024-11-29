from . import entity
import pygame as pyg

class Player(entity.Entity):
    def __init__(this, position, image_path, speed_mag, *groups):
        super().__init__(position, image_path, speed_mag, *groups)
    
    def update(this, dt, __test_var=None):
        this.player_movement_logic()
        super().update(dt)
    
    def player_movement_logic(this):
        # mouse_pos = pyg.mouse.get_pos()
        
        # if mouse_pos == this.rect.center:
        #     this.velocity = pyg.math.Vector2(0, 0)

        # this.rotate_towards_pos(mouse_pos)
        # this.move_towards_pos(mouse_pos)
        
        # wasd movement
        keys = pyg.key.get_pressed()
        if keys[pyg.K_w]:
            this.velocity.y = -this.magnitude_speed
            this.velocity.x = 0
        if keys[pyg.K_s]:
            this.velocity.y = this.magnitude_speed
            this.velocity.x = 0
        if keys[pyg.K_a]:
            this.velocity.x = -this.magnitude_speed
            this.velocity.y = 0
        if keys[pyg.K_d]:
            this.velocity.x = this.magnitude_speed
            this.velocity.y = 0
        if keys[pyg.K_SPACE]:
            this.velocity *= 0