import pygame as pyg
import dataclasses
import sys
import time
import math
import copy
import random

pyg.init()

all_entities = []

def blit_text(surface: pyg.Surface, text, pos, color=pyg.Color('black'), font_size=32):
    font = pyg.font.SysFont("Arial", font_size)
    text = font.render(text, True, color)
    surface.blit(text, pos)

class Entity(pyg.sprite.DirtySprite):
    def __init__(self, image_path, velocity, *groups):
        super().__init__(*groups)
        self.image = pyg.image.load(image_path).convert_alpha()
        self.image_path = image_path
        self.rect = self.image.get_rect()
        self.group = pyg.sprite.GroupSingle()
        
        self.rot_an = 90;
        self.type = 'normal'
        
        self.velocity = pyg.Vector2(velocity)
        
        self.group.add(self)
        all_entities.append(self)
    
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
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - self.rot_an
        self.image = pyg.transform.rotate(pyg.image.load(self.image_path).convert_alpha(), angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def rotate_towards(self, pos):
        rel_x, rel_y = pos[0] - self.rect.centerx, pos[1] - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - self.rot_an
        self.image = pyg.transform.rotate(pyg.image.load(self.image_path).convert_alpha(), angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def instantiate(self):
        return copy.deepcopy(self)

class Henchman(Entity):
    def __init__(self, image_path, velocity, *groups):
        super().__init__(image_path, velocity, *groups)
        self.prev_time = time.time()
        self.type = "henchman"
    def update(self):
        for r in all_entities:
            if r.type == "knife":
                if self.rect.colliderect(r.rect):
                    if self in all_entities:
                        all_entities.remove(self)
                    self.kill()
                    break
        self.move()
        if self in self.group:
            self.group.remove(self)
            self.group.update()
            self.group.add(self)
        else:
            self.group.update()
        self.group.draw(pyg.display.get_surface())
        
    

class SpawnerOfHenchmen:
    def __init__(self):
        self.henchmen = []
        self.prev_time = time.time()
        self.spawn_rate = 3
    
    def update(self, dt):
        if time.time() - self.prev_time > self.spawn_rate:
            new_henchman = Henchman("assets/sprites/henchman1.png", (0, 0))
            new_henchman.rect.center = (random.randint(0, int(WIDTH)), 0)
            new_henchman.rotate_towards(player.rect.center)
            
            hench_pos = pyg.Vector2(new_henchman.rect.center)
            direction = pyg.Vector2(player.rect.center) - hench_pos
            if direction.length() > 0:
                direction = direction.normalize()
            new_henchman.velocity = direction * 300 * dt
            
            self.henchmen.append(new_henchman)
            
            
            self.prev_time = time.time()
        for henchman in self.henchmen:
            henchman.update()

is_running = True
WIDTH = 900
HEIGHT = 500
screen = pyg.display.set_mode((WIDTH, HEIGHT))

pyg.event.set_grab(True)
pyg.mouse.set_visible(True)
        
player = Entity("assets/sprites/Player.png", (0, 0))
player.type = "player"
henchman1 = Entity("assets/sprites/henchman1.png", (0, 0))
knife = Entity("assets/sprites/knife.png", (0, 0))
knife.type = "knife"
knife.rot_an = 45
clock = pyg.time.Clock()


def move_tha_player(dt):
    mouse_pos = pyg.mouse.get_pos()
    player_pos = pyg.Vector2(player.rect.center)
    direction = pyg.Vector2(mouse_pos) - player_pos
    if direction.length() > 0:
        direction = direction.normalize()
    velocity = 250
    player.velocity = direction * velocity * dt

def make_tha_knife_throw(dt):
    global knife
    mouse_pos = pyg.mouse.get_pos()
    player_pos = pyg.Vector2(player.rect.center)
    direction = pyg.Vector2(mouse_pos) - player_pos
    if direction.length() > 0:
        direction = direction.normalize()
    velocity = 600
    new_knife = knife.instantiate()
    new_knife.type = "knife"
    new_knife.rect.center = player.rect.center
    new_knife.velocity = direction * velocity * dt
    new_knife.rotate_towards_mouse()
    all_entities.append(new_knife)
    runtime_objs.append(new_knife)
    
runtime_objs = []
spawner = SpawnerOfHenchmen()

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

    for ent in all_entities:
        if ent.type == "henchman":
            if player.rect.colliderect(ent.rect):
                if player in all_entities:
                    all_entities.remove(player)
                player.kill()
    spawner.update(dt)

    for obj in runtime_objs:
        obj.update()
    blit_text(screen, str(dt), (10, 10))  
    blit_text(screen, str(all_entities), (10, 30), font_size=12)
    pyg.display.update()
            
            
pyg.quit()
sys.exit(69)