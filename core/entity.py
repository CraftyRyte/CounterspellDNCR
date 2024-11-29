import pygame as pyg
import math

class Entity(pyg.sprite.Sprite):
    def __init__(this, position: tuple, image_path:str, speed_magnitude, *groups):
        super().__init__(*groups)
        this.magnitude_speed = speed_magnitude
        this.position = pyg.math.Vector2(position)
        this.image = pyg.image.load(image_path).convert_alpha()
        this.image_path = image_path
        this.og_image = this.image
        
        this.rect = this.image.get_frect(center=this.position)
        this.__display_surface__: pyg.Surface = pyg.display.get_surface()
        
        this.velocity = pyg.math.Vector2(0, 0)

    def update(this, dt):
        this.__display_surface__: pyg.Surface = pyg.display.get_surface()
        this.move(dt)
    
    def move(this, dt):
        this.position += this.velocity * dt
        this.rect.center = this.position
    
    def rotate(this, angle):
        this.image = pyg.transform.rotate(this.og_image, angle)
        this.rect = this.image.get_frect(center=this.position)
    
    @staticmethod
    def determine_rotation_angles(pos_tm: tuple, entity_pos, rotational_offset=0):
        mx, my = pos_tm
        px, py = entity_pos
        dy,dx = mx - px,my - py
        radians = math.atan2(dy, dx)
        angles = (180 / math.pi) * radians + rotational_offset
        return angles

    def rotate_towards_pos(this, pos):
        angles = this.determine_rotation_angles(pos, this.rect.center, 180)
        this.rotate(angles)
    
    def  move_towards_pos(this, pos):
        mousex, mousey = pos

        direction = pyg.math.Vector2(mousex - this.position.x, mousey - this.position.y).normalize()

        this.velocity = direction * this.magnitude_speed

        
