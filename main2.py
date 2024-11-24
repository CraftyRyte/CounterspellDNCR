import pygess as gess
import pygame as pyg

world = gess.physics.World((0, 0))
gess.physics.set_active_world(world)

# Screen settings
WIDTH, HEIGHT = 900, 500
screen = pyg.display.set_mode((WIDTH, HEIGHT))
clock = pyg.time.Clock()

player = gess.entity.MovingEntity((0, 0), (64, 64), (0, 0), image_path='assets/sprites/player.png')
world.add_gameobj(player)

def move

# Main loop
while True:
    gess.physics.update_delta_time()
    screen.fill(pyg.Color('white'))
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            exit()
    gess.physics.update_worlds()
    pyg.display.flip()
    clock.tick(60)


