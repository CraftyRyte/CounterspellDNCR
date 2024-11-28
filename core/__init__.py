from . import entity
from . import player
from . import henchman
from . import spawner
from . import camera
import pygame as pyg

def blit_text(surface, text, pos, color=pyg.Color("black"), font_size=32):
    font = pyg.font.SysFont("Arial", font_size)
    text_surf = font.render(str(text), True, color)
    surface.blit(text_surf, pos)

def is_wrong_range(range:tuple):
    return not range[0] >= range[1]