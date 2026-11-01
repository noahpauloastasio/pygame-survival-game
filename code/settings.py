import pygame
from asset_loader import import_folder

WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

ITEM_BOX_SIZE = 70
UI_BG_COLOUR = (60,60,60)
BORDER_COLOUR =(30, 30, 30)
BORDER_GLOW = (240,200, 40)
BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
GREY = (104, 104, 104)
RED = (255, 0, 0)

# main menu
button_height = 60
button_width = 200

HITBOX_OFFSET = {'grass': 10, 'player': 2, 'object':10}


enemy_data = {
    'basic zombie': {
        'health': 60,
        'speed': 2,
        'damage': 10,
        'image_path': '../graphics/enemies/zombie',
        'notice_radius': 300,
        'attack_radius': 30,
        'attack_cooldown':600,
        'exp_gain':10
        }
}

enemy_zones = {
    'basic zombie': [
        {
            'area': pygame.Rect(200, 200, 400, 400),
            'count': 1,
        }
    ]
}

