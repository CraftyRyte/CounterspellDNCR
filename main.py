import pygame as pyg
import dataclasses
import sys
import time

pyg.init()

def blit_text(surface: pyg.Surface, text, pos, color=pyg.Color('black')):
    font = pyg.font.SysFont("Arial", 32)
    text = font.render(text, True, color)
    surface.blit(text, pos)

class Entity(pyg.sprite.DirtySprite):
    def __init__(self, image_path, velocity, *groups):
        super().__init__(*groups)
        self.image = pyg.image.load(image_path).convert_alpha()
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

is_running = True
WIDTH = 900
HEIGHT = 500
screen = pyg.display.set_mode((WIDTH, HEIGHT))
        
player = Entity("assets/sprites/Player.png", (0, 0))
knife = Entity("assets/sprites/knife.png", (0, 0))
clock = pyg.time.Clock()


def move_tha_player(dt):
    keys = pyg.key.get_pressed()
    velocity = 200
    if keys[pyg.K_w]:
        player.velocity.y = -velocity * dt
        player.velocity.x = 0
    if keys[pyg.K_s]:
        player.velocity.y = velocity * dt
        player.velocity.x = 0
    if keys[pyg.K_a]:
        player.velocity.x = -velocity * dt
        player.velocity.y = 0
    if keys[pyg.K_d]:
        player.velocity.x = velocity * dt
        player.velocity.y = 0
    

while is_running:

    dt = clock.tick(60) / 1000
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            is_running = False

    screen.fill('white')
            
    player.update()
    move_tha_player(dt)
    blit_text(screen, str(dt), (10, 10))  
    pyg.display.update()
            
            
pyg.quit()
sys.exit(69)