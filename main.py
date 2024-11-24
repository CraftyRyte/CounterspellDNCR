import pygame as pyg
import dataclasses
import sys
import time
import math
import copy

pyg.init()

def blit_text(surface: pyg.Surface, text, pos, color=pyg.Color('black')):
    font = pyg.font.SysFont("Arial", 32)
    text = font.render(text, True, color)
    surface.blit(text, pos)

class Entity(pyg.sprite.DirtySprite):
    def __init__(self, image_path, velocity, *groups):
        super().__init__(*groups)
        self.image = pyg.image.load(image_path).convert_alpha()
        self.image_path = image_path
        self.rect = self.image.get_rect()
        self.group = pyg.sprite.GroupSingle()
        
        self.velocity = pyg.Vector2(velocity)
        
        self.group.add(self)
    
    def update(self):
        self.move()
        if self in self.group:
            self.group.remove(self)
            self.group.update()
            self.group.add(self)
        else:
            self.group.update()
        self.group.draw(pyg.display.get_surface())

    def move(self):
        self.rect.center += self.velocity

    def rotate_towards_mouse(self):
        mouse_pos = pyg.mouse.get_pos()
        rel_x, rel_y = mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        self.image = pyg.transform.rotate(pyg.image.load(self.image_path).convert_alpha(), angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def instantiate(self):
        return copy.deepcopy(self)

is_running = True
WIDTH = 900
HEIGHT = 500
screen = pyg.display.set_mode((WIDTH, HEIGHT))

pyg.event.set_grab(True)
pyg.mouse.set_visible(True)
        
player = Entity("assets/sprites/Player.png", (0, 0))
knife = Entity("assets/sprites/knife.png", (0, 0))
clock = pyg.time.Clock()


def move_tha_player(dt):
    mouse_pos = pyg.mouse.get_pos()
    player_pos = pyg.Vector2(player.rect.center)
    direction = pyg.Vector2(mouse_pos) - player_pos
    if direction.length() > 0:
        direction = direction.normalize()
    velocity = 200
    player.velocity = direction * velocity * dt

def make_tha_knife_throw(dt):
    global knife
    mouse_pos = pyg.mouse.get_pos()
    player_pos = pyg.Vector2(player.rect.center)
    direction = pyg.Vector2(mouse_pos) - player_pos
    if direction.length() > 0:
        direction = direction.normalize()
    velocity = 500
    new_knife = knife.instantiate()
    new_knife.rect.center = player.rect.center
    new_knife.velocity = direction * velocity * dt
    new_knife.rotate_towards_mouse()
    runtime_objs.append(new_knife)
    
runtime_objs = []

while is_running:

    dt = clock.tick(60) / 1000
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            is_running = False
        if event.type == pyg.MOUSEBUTTONDOWN:
            if event.button == 1:
                make_tha_knife_throw(dt)

    screen.fill('white')
            
    player.update()
    player.rotate_towards_mouse()
    move_tha_player(dt)

    for obj in runtime_objs:
        obj.update()
    blit_text(screen, str(dt), (10, 10))  
    pyg.display.update()
            
            
pyg.quit()
sys.exit(69)