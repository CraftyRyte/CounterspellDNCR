import pygame as pyg
from .. import entity as ent
from .. import player as plr
import copy 
import time


class SpawnEntity:
    def __init__(this, spawn_entity: ent.Entity, spawn_rate: float):
        this.entity = spawn_entity
        this.spawn_rate = spawn_rate
        this.entities_spawned = []

        this.prev_time = time.time()

    def update(this, dt, group):
        from .. import util_funcs as uf

        if time.time() - this.prev_time >= this.spawn_rate:
            this.spawn_entity(group)
            this.prev_time = time.time()
        return
    
    def spawn_entity(this, group):
        new_ent = copy.deepcopy(this.entity)
        group.add(new_ent)
        this.entities_spawned.append(new_ent)
        
