import pygame
from settings import *
from betaTile import Tile
from player import Player
from asset_loader import import_folder
from random import choice
import pytmx
from pytmx.util_pygame import load_pygame
from ui import UI
from enemy import Enemy
import random


class Level:
    def __init__(self, difficulty_multiplier):
        self.difficulty_multiplier = difficulty_multiplier
        # access the active game screen for drawing
        self.display_surface = pygame.display.get_surface()
        self.day = 1

        # create groups to manage different types of sprites
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.projectiles = CameraGroup()

        self.attack_hitbox_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.player_start_pos = (800,700)

        self.player = Player(
            self.player_start_pos,
            [self.visible_sprites],    
            self.obstacle_sprites,
            self.attack_hitbox_sprites,
            self.attackable_sprites,
            self.visible_sprites,
            self
        )
        self.ui = UI(self.player)
        self.visible_sprites.change_layer(self.player, 2)   # move player to layer 2

        self.tmx_data = load_pygame("../map/postap_map.tmx")
        self.build_world()
        self.spawn_enemy('basic zombie')

        self.loot = ['soda', 'mre', 'peas', 'syringe', 'bullets']

    def build_world(self):

        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)

                    if tile_image:
                        # Scale tile to match the game's TILESIZE
                        tile_image = pygame.transform.scale(tile_image, (TILESIZE, TILESIZE))

                        # Convert tile grid coordinates → world pixel coordinates
                        world_x = x * TILESIZE
                        world_y = y * TILESIZE

                        tile_sprite = Tile(
                            (world_x, world_y),
                            tile_image,
                            [self.visible_sprites]
                        )

                        # Ground tiles drawn on the lowest layer
                        self.visible_sprites.change_layer(tile_sprite, 0)


            # --- VISIBLE TILE LAYERS (GROUND + DECORATION) ---
            for layer in self.tmx_data.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid in layer:
                        tile_image = self.tmx_data.get_tile_image_by_gid(gid)

                        if tile_image:
                            # scale tile to match in‑game TILESIZE
                            tile_image = pygame.transform.scale(tile_image, (TILESIZE, TILESIZE))

                            tile_sprite = Tile(
                                (x * TILESIZE, y * TILESIZE),
                                tile_image,
                                [self.visible_sprites]
                            )
                            self.visible_sprites.change_layer(tile_sprite, 0)

            # collision layer - invisible
            try:
                collision_obj_layer = self.tmx_data.get_layer_by_name("CollisionObjects")

                scale_x = TILESIZE / self.tmx_data.tilewidth
                scale_y = TILESIZE / self.tmx_data.tileheight

                for obj in collision_obj_layer:
                    hitbox_x = obj.x * scale_x
                    hitbox_y = obj.y * scale_y
                    hitbox_w = obj.width * scale_x
                    hitbox_h = obj.height * scale_y

                    if hitbox_h > TILESIZE *2:
                        final_y = hitbox_y
                    else:
                        final_y = hitbox_y - hitbox_h

                    collision_sprite = Tile(
                        (hitbox_x, hitbox_y),
                        None,
                        [self.obstacle_sprites]
                    )

                    # ensure we use top left corner rather than bottom like for tiles
                    collision_sprite.rect = pygame.Rect(hitbox_x, final_y, hitbox_w, hitbox_h)
                    collision_sprite.hitbox = collision_sprite.rect.copy()
            except:
                print("No CollisionObjects layer found")

            # --- PROPS LAYER (OBJECTS WITH PNGs) ---
            try:
                props_layer = self.tmx_data.get_layer_by_name("Props")

                # scale factor between TMX tile size and your TILESIZE
                scale_x = TILESIZE / self.tmx_data.tilewidth
                scale_y = TILESIZE / self.tmx_data.tileheight

                for obj in props_layer:
                    if obj.image:

                        # scale image to match object width/height in tiles
                        scaled_width = int(obj.width * scale_x)
                        scaled_height = int(obj.height * scale_y)

                        image = pygame.transform.scale(obj.image, (scaled_width, scaled_height))

                        # convert TMX pixel coords → scaled game coords
                        prop_x = obj.x * scale_x
                        prop_y = obj.y * scale_y

                        # anchor fix: place bottom of object on correct tile
                        prop_sprite = Tile(
                            (prop_x, prop_y - scaled_height),
                            image,
                            [self.visible_sprites]
                        )

                        self.visible_sprites.change_layer(prop_sprite, 1)

            except:
                print("No props layer found in TMX")

    def spawn_enemy(self, enemy_type):
        # get all zones for this enemy type
        zones = enemy_zones.get(enemy_type, [])


        for zone in zones:
            area = zone['area']
            count = zone['count']

            enemy_count = count + (self.day)

            for i in range(enemy_count):
                x = random.randint(area.left, area.right)
                y = random.randint(area.top, area.bottom)

                Enemy(
                    enemy_type,
                    self.player,
                    (x, y),
                    [self.visible_sprites,
                    self.attackable_sprites],
                    self.obstacle_sprites,
                    self.difficulty_multiplier,
                    self
                )

    def start_next_day(self):
        self.day += 1
        self.day_transition()

        if self.day == 3:
            self.player.add_to_inventory('pistol')

        self.player.hitbox.center = self.player_start_pos
        self.player.rect.center = self.player.hitbox.center
        #self.player.direction = pygame.Vector2()
        self.player.health = self.player.current_max_stats['health']
        self.player.energy = self.player.current_max_stats['energy']
        

        self.spawn_enemy('basic zombie')

    def fade(self):
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))

        for alpha in range(0, 255, 5):
            fade_surface.set_alpha(alpha)
            self.display_surface.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(20)
    
    def day_transition(self):
        self.fade()

        font = pygame.font.Font(None, 80)
        text = font.render(f"Day {self.day}", True, WHITE)
        rect = text.get_rect(center = (WIDTH//2, HEIGHT//2))

        self.display_surface.blit(text, rect)
        pygame.display.update()
        pygame.time.delay(1500)

    def game_over(self):
        self.fade()

        # game over message
        font = pygame.font.Font(None, 100)
        text = font.render("GAME OVER", True, RED)
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
        self.display_surface.blit(text, rect)

        small_font = pygame.font.Font(None, 60)
        survived_text = small_font.render(f"You survived {self.day} days", True, WHITE)
        survived_rect = survived_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
        self.display_surface.blit(survived_text, survived_rect)

        pygame.display.update()
        pygame.time.delay(2000)

        # reset game
        self.day = 1
        self.player.exp_level = 0
        self.player.exp = 0

        self.player.hitbox.center = self.player_start_pos
        self.player.rect.center = self.player.hitbox.center
        
        self.player.inventory = ['dagger', '', '', '', '']
        self.player.health = self.player.current_max_stats['health']
        self.player.energy = self.player.current_max_stats['energy']
        self.player.speed = self.player.current_max_stats['speed']

        self.clear_enemies()
        self.spawn_enemy('basic zombie')

    def clear_enemies(self):
        for sprite in self.attackable_sprites:
            if hasattr(sprite, "enemy_type"):  
                sprite.kill()

    def drop_loot(self):
        if random.random() < 0.4: # 40% chance of loot drop
            item = random.choice(self.loot)
            if item == 'bullets':
                self.player.bullets = min(self.player.bullets + 5, self.player.max_bullets)
            else:
                self.player.add_to_inventory(item)

    def run(self):
        if self.player.health <= 0:
            self.game_over()
            return
        # draw everything else
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update(self.player)
        self.projectiles.update()
        self.ui.display(self.player)

        for enemy in self.attackable_sprites:
            enemy.draw_health_bar(self.display_surface, self.visible_sprites.offset)

        if len(self.attackable_sprites) == 0:
            self.start_next_day()


class CameraGroup(pygame.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # centre the camera on the player
        self.offset.x = player.rect.centerx - WIDTH // 2
        self.offset.y = player.rect.centery - HEIGHT // 2

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
