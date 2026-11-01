import pygame
from settings import *
class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        # bar sizes and colours
        self.health_bar_width = 180 + (player.current_max_stats["health"] - 100)
        self.energy_bar_width = 130 + (player.current_max_stats["energy"] - 100)
        self.bar_height = 20
        self.health_y = HEIGHT - self.bar_height - 20
        self.bar_bg_colour = (60, 60, 60)
        self.health_fg_colour = (200, 0, 0)
        self.energy_fg_colour = (120, 67, 0)

        self.font = pygame.font.Font(None, 24)
        self.exp_bar_width = 100

        self.exp_x = WIDTH - self.exp_bar_width - 20
        self.exp_y = HEIGHT - self.bar_height - 20

        self.energy_y = self.health_y - self.bar_height - 5

        self.item_icons = {
            'dagger': pygame.image.load('../graphics/item_icons/dagger.png').convert_alpha(),
            'pistol': pygame.image.load('../graphics/item_icons/pistol.png').convert_alpha(),
            'soda': pygame.image.load('../graphics/item_icons/soda.png').convert_alpha(),
            'mre': pygame.image.load('../graphics/item_icons/mre.png').convert_alpha(),
            'syringe': pygame.image.load('../graphics/item_icons/syringe.png').convert_alpha(),
            'peas': pygame.image.load('../graphics/item_icons/peas.png').convert_alpha()
        }


    def draw_bar(self, surface, x, y, current, max, width, height, fg, bg):
        # background bar
        pygame.draw.rect(surface, bg, (x, y, width, height))
        # border
        pygame.draw.rect(surface, (200, 200, 200), (x,y, width, height), 3)
        # current stat bar
        ratio = current / max
        pygame.draw.rect(surface, fg, (x+3, y+3, int((width-6) * ratio), height-6))


    def inventory(self, player):
        x_pos = 1200 // 2 - (ITEM_BOX_SIZE * 5 // 2)
        inventory_rects = []

        for i in range(5):
            rect = pygame.Rect(x_pos + i * (ITEM_BOX_SIZE + 10), 635, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
            pygame.draw.rect(self.display_surface, UI_BG_COLOUR, rect)
            
            if i==player.selected_index:
                colour = BORDER_GLOW
            else:
                colour = BORDER_COLOUR

            pygame.draw.rect(self.display_surface, colour, rect, 3)

            if i <len(player.inventory):
                item = player.inventory[i]

                if item:
                    icon = self.item_icons[item]
                    icon = pygame.transform.scale(icon, (ITEM_BOX_SIZE -12, ITEM_BOX_SIZE - 12))
                    icon_rect = icon.get_rect(center=rect.center)
                    self.display_surface.blit(icon, icon_rect)
                    
                    if item == "pistol":
                        font = pygame.font.SysFont("consolas", 18)
                        count = font.render(str(player.bullets), True, WHITE)

                        x = rect.right - count.get_width() - 4
                        y = rect.bottom - count.get_height() - 4

                        self.display_surface.blit(count, (x,y))

            inventory_rects.append(rect)

        return inventory_rects
    
        
    def display(self, player):
        # health bar
        self.draw_bar(
            surface=self.display_surface,
            x=20, y=self.health_y,
            current=player.health,
            max=player.current_max_stats["health"],
            width=self.health_bar_width,
            height=self.bar_height,
            fg=self.health_fg_colour,
            bg=self.bar_bg_colour
        )
        # energy bar
        self.draw_bar(
            surface=self.display_surface,
            x=20, y=self.energy_y,
            current=player.energy,
            max=player.current_max_stats["energy"],
            width=self.energy_bar_width,
            height=self.bar_height,
            fg=self.energy_fg_colour,
            bg=self.bar_bg_colour
        )
        # exp bar
        self.draw_bar(
            surface=self.display_surface,
            x=self.exp_x,
            y=self.exp_y,
            current=player.exp,
            max=player.exp_next_rank,
            width=self.exp_bar_width,
            height=self.bar_height,
            fg=(0, 160, 60),   
            bg=(40, 40, 40)      
        )

        # level 
        level_surf = self.font.render(str(player.exp_level), True, (255, 255, 255))
        level_rect = level_surf.get_rect(center=(WIDTH - 70, HEIGHT-50))
        self.display_surface.blit(level_surf, level_rect)
        
        self.inventory(player)


