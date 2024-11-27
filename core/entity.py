import pygame as pyg
import math

class Entity(pyg.sprite.Sprite):
    def __init__(self, position: tuple, image_path:str):
        super().__init__()
        self.position = pyg.math.Vector2(position)
        self.image = pyg.image.load(image_path).convert_alpha()
        self.og_image = self.image
        
        self.rect = self.image.get_frect(center=self.position)
        self.group = pyg.sprite.GroupSingle(self)
        self.__display_surface__: pyg.Surface = pyg.display.get_surface()
        
        self.velocity = pyg.math.Vector2(0, 0)

    def update(self, dt):
        self.__display_surface__: pyg.Surface = pyg.display.get_surface()
        self.__display_surface__.blit(self.image, self.rect)
        self.move(dt)
    
    def move(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position
    
    def rotate(self, angle):
        self.image = pyg.transform.rotate(self.og_image, angle)
        self.rect = self.image.get_frect(center=self.position)
    
    @staticmethod
    def determine_rotation_angles(pos_tm: tuple, entity_pos):
        mx, my = pos_tm
        px, py = entity_pos
        ydiff = mx - px
        xdiff = my - py
        radians = math.atan2(ydiff, xdiff)
        angles = (180 / math.pi) * radians + 180
        return angles

        
