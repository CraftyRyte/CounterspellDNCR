import pygame as pyg
from .. import entity as ent
from .. import player as plr
from . import spawner as spw



class HenchmanSpawner(spw.SpawnEntity):
    def __init__(this, henchman_prefab, spawn_rate, spawn_radius=None):
        super().__init__(henchman_prefab, spawn_rate)
        this.spawn_radius = spawn_radius
    
    def update(this, dt, player_center, surface, group):
        import time
        
        if time.time() - this.prev_time >= this.spawn_rate:
            this.spawn_entity(player_center, surface, group)
            this.prev_time = time.time()
            
    #TODO: Simplify, break into more functions
    def spawn_entity(this, player_center, surface, group):
        import copy
        import random as rnd
        
        abscissa_range = this.get_spawn_range(player_center, surface, this.spawn_radius)[0]
        ordinate_range = this.get_spawn_range(player_center, surface, this.spawn_radius)[1]
        
        new_ent: ent.Entity = copy.deepcopy(this.entity)
        
        rand_x = rnd.randint(abscissa_range[0], abscissa_range[1])
        rand_y = rnd.randint(ordinate_range[0], ordinate_range[1])
        
        new_ent.rect.center = (rand_x, rand_y)
        group.add(new_ent)

        this.entities_spawned.append(new_ent)
    
    @staticmethod
    #TODO: Write test for this functions
    def get_spawn_range(player_center, surface: pyg.Surface, spawn_radius=None) -> tuple[tuple, tuple]:
        from .. import is_wrong_range
        #TODO: Rewrite using no nesting
        radius = spawn_radius
        if spawn_radius == None:
            w, h = surface.get_size()
            
            if w < h:
                radius = w
            elif h < w:
                radius = h
            else:
                radius = w
        
        # no neg check
        radius = abs(radius)
        
        y_range = (int(player_center[1] - radius), int(player_center[1] + radius))
        x_range = (int(player_center[0] - radius), int(player_center[0] + radius))
    
        return (x_range, y_range)

