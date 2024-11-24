import pygame as pyg
import sys
import time
import math
import random
from pygame.math import Vector2

# Initialize Pygame
pyg.init()
pyg.mixer.init()

# Screen settings
WIDTH, HEIGHT = 900, 500
screen = pyg.display.set_mode((WIDTH, HEIGHT))
clock = pyg.time.Clock()

knife_t = "knife_throw.mp3"
ezio_s = "ezio_scream.mp3"
henchman_s = "henchman_scream.mp3"
 
# Global variables
all_entities = []
runtime_objs = []

# Helper function to render text on screen
def blit_text(surface, text, pos, color=pyg.Color('black'), font_size=32):
    font = pyg.font.SysFont("Arial", font_size)
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)

# Add the Camera class
class Camera:
    def __init__(self):
        self.offset = Vector2(0, 0)
    
    def update(self, target):
        # Center the camera on the target (player)
        self.offset.x = target.rect.centerx - WIDTH / 2
        self.offset.y = target.rect.centery - HEIGHT / 2

# Entity base class
class Entity(pyg.sprite.DirtySprite):
    def __init__(self, image_path, velocity, *groups):
        super().__init__(*groups)
        self.image = pyg.image.load(image_path).convert_alpha()
        self.image_path = image_path
        self.rect = self.image.get_rect()
        self.velocity = Vector2(velocity)
        self.type = 'normal'
        self.is_alive = True
        self.mask = pyg.mask.from_surface(self.image)
        all_entities.append(self)

    def update(self):
        self.move()               
        self.draw(camera)

    def move(self):
        self.rect.center += self.velocity

    def draw(self, camera):
        # Adjust position based on camera offset
        adjusted_rect = self.rect.move(-camera.offset.x, -camera.offset.y)
        screen.blit(self.image, adjusted_rect)

    def rotate_towards(self, target_pos):
        rel_x, rel_y = target_pos[0] - self.rect.centerx, target_pos[1] - self.rect.centery
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x) - 90
        self.image = pyg.transform.rotate(pyg.image.load(self.image_path).convert_alpha(), angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pyg.mask.from_surface(self.image)

    def instantiate(self):
        return self.__class__(self.image_path, self.velocity)

    def kill(self):
        self.is_alive = False
        super().kill()

# Henchman subclass
class Henchman(Entity):
    def __init__(self, image_path, velocity):
        super().__init__(image_path, velocity)
        self.type = "henchman"
        # Reduce the size of the rect to make the hitbox smaller
        self.rect.inflate_ip(-10, -10)

    def update(self):
        # Use per-pixel collision detection
        if self.rect.colliderect(player.rect):
            pyg.mixer.music.load(ezio_s)
            pyg.mixer.music.play()
            all_entities.remove(self)
            self.kill()
        for obj in all_entities:
            if obj.type == "knife" and self.rect.colliderect(obj.rect):
                pyg.mixer.music.load(henchman_s)
                pyg.mixer.music.play()
                all_entities.remove(self)
                all_entities.remove(obj)
                if obj in runtime_objs:
                    runtime_objs.remove(obj)
                obj.kill()
                self.kill()
                break
        self.move()
        self.rotate_towards(player.rect.center)
        direction = (Vector2(player.rect.center) - Vector2(self.rect.center)).normalize()
        self.velocity = direction * 620 * dt
        adjusted_rect = self.rect.move(-camera.offset.x, -camera.offset.y)
        self.draw(camera)

# Spawner class for generating henchmen
class SpawnerOfHenchmen:
    def __init__(self):
        self.henchmen = []
        self.spawn_rate = 3
        self.prev_time = time.time()

    def update(self, dt):
        if time.time() - self.prev_time > self.spawn_rate:
            new_henchman = Henchman("assets/sprites/henchman1.png", (0, 0))
            new_henchman.rect.center = (random.randint(0, WIDTH), 0)
            new_henchman.rotate_towards(player.rect.center)
            direction = (Vector2(player.rect.center) - Vector2(new_henchman.rect.center)).normalize()
            new_henchman.velocity = direction * 620 * dt
            self.henchmen.append(new_henchman)
            all_entities.append(new_henchman)
            self.prev_time = time.time()

        # Update henchmen and remove any that are killed
        for henchman in self.henchmen[:]:
            if not henchman.is_alive:
                self.henchmen.remove(henchman)
            else:
                henchman.update()

# Player control functions
def move_player(dt):
    mouse_pos = pyg.mouse.get_pos()
    world_mouse_pos = Vector2(mouse_pos) + camera.offset
    direction_vector = world_mouse_pos - Vector2(player.rect.center)
    if direction_vector.length() != 0:
        direction = direction_vector.normalize()
        player.velocity = direction * 250 * dt
    else:
        player.velocity = Vector2(0, 0)

def throw_knife(dt):
    mouse_pos = pyg.mouse.get_pos()
    world_mouse_pos = Vector2(mouse_pos) + camera.offset
    direction = (world_mouse_pos - Vector2(player.rect.center)).normalize()
    new_knife = knife.instantiate()
    new_knife.rect.center = player.rect.center
    new_knife.type = "knife"
    new_knife.velocity = direction * 1200 * dt
    new_knife.rotate_towards(world_mouse_pos)
    all_entities.append(new_knife)
    runtime_objs.append(new_knife)
    pyg.mixer.music.load(knife_t)
    pyg.mixer.music.play()


# Instantiate player and other entities
player = Entity("assets/sprites/Player.png", (0, 0))
player.type = "player"
knife = Entity("assets/sprites/knife.png", (0, 0))
knife.type = "knife"
spawner = SpawnerOfHenchmen()
spawner.spawn_rate = 2

# Instantiate the camera
camera = Camera()

# Main game loop
is_running = True
while is_running:
    dt = clock.tick(60) / 1000  # Delta time for frame-rate independent movement

    # Event handling
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            is_running = False
        elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
            throw_knife(dt)

    # Update entities and handle player movement
    camera.update(player)
    screen.fill('white')
    screen.blit(pyg.image.load("Sprite-0007.png"), (0, 0))
    if dt > 0:
        move_player(dt)
    player.update()
    world_mouse_pos = Vector2(pyg.mouse.get_pos()) + camera.offset
    player.rotate_towards(world_mouse_pos)
    player.draw(camera)


    # Update henchmen and check for collisions with the player
    spawner.update(dt)
    for ent in all_entities:
        if ent.type == "henchman" and pyg.sprite.collide_mask(player, ent):
            if player in all_entities:
                all_entities.remove(player)
            player.kill()

    # Update runtime objects (like knives)
    for obj in runtime_objs:
        obj.update()
        obj.draw(camera)

    # Display debug info
    blit_text(screen, f"FPS: {clock.get_fps():.2f}", (10, 10))
    pyg.display.update()

# Clean up
pyg.quit()
sys.exit()
