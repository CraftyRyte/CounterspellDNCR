import pygame as pyg

class Cam3DEffect(pyg.sprite.Group):
    def __init__(this, ground_path, *sprites):
        super().__init__(*sprites)
        this.display_surface = pyg.display.get_surface()
        
        this.camera_offset = pyg.Vector2(0, 0)
        this.half_w = this.display_surface.get_width()/2
        this.half_y = this.display_surface.get_height()/2
        
        this.ground_img = pyg.image.load(ground_path).convert()
        this.ground_rect = this.ground_img.get_frect()
    
    def center_target_camera(this, target):
        this.camera_offset.x = target.rect.centerx - this.half_w
        this.camera_offset.y = target.rect.centery - this.half_y
    
    def draw(this, player):
        this.center_target_camera(player)
        
        # ground
        ground_offset = this.ground_rect.topleft - this.camera_offset
        this.display_surface.blit(this.ground_img, ground_offset)
        
        for sprite in sorted(this.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - this.camera_offset 
            this.display_surface.blit(sprite.image, offset_pos )
