import pygame as pyg
import sys
import core
import time
import math

import core.henchman

# Initialize pyg
pyg.init()

width, height = 900, 500
if __name__ == "__main__":
    screen = pyg.display.set_mode((width, height))
pyg.display.set_caption("pyg Boilerplate")

player = core.player.Player((width / 2, height / 2), "assets/sprites/Player.png", 390)
player.velocity = pyg.math.Vector2(0, 0)

# Entity Spawner test
test_spawner = core.spawner.henchman_spawner.HenchmanSpawner(core.henchman.Henchman((width/2, height/2), "assets/sprites/henchman1.png", 300), 4, 50)

# Main game loop
running = True
not_overlapping = True
clock = pyg.time.Clock()
prev_time = time.time()

if __name__ == "__main__":
    while running:
        dt = time.time() - prev_time
        prev_time = time.time()

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False

        # Fill the screen with a color (RGB)
        screen.fill((255, 255, 255))

        player.group.update(dt)
        test_spawner.update(dt, player.rect.center, screen)
        core.blit_text(screen, clock.get_fps(), (10, 10))

        # Update the display
        pyg.display.flip()

        # Cap the frame rate at 60 FPS
        clock.tick(60)

# Quit pyg
pyg.quit()
sys.exit()
