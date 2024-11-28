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

    def update(this, dt):
        from .. import util_funcs as uf

        if time.time() - this.prev_time >= this.spawn_rate:
            this.spawn_entity()
            this.prev_time = time.time()
        for entity in this.entities_spawned:
            entity.group.update(dt)

    def spawn_entity(this):
        new_ent = copy.deepcopy(this.entity)
        this.entities_spawned.append(new_ent)
        
