import pygame as pyg

class Cam3DEffect(pyg.sprite.Group):
    def __init__(this, *sprites):
        super().__init__(*sprites)
        this.display_surface = pyg.display.get_surface()
        
        this.camera_offset = pyg.Vector2(0, 0)
        this.half_w = this.display_surface.get_width()/2
        this.half_y = this.display_surface.get_height()/2
    
    def center_target_camera(this, target):
        this.camera_offset.x = target.rect.centerx - this.half_w
        this.camera_offset.y = target.rect.centery - this.half_y
    
    def draw(this):
        
        for sprite in sorted(this.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - this.camera_offset 
            this.display_surface.blit(sprite.image, offset_pos )
