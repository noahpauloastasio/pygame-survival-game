import pygame
from settings import *
from entity import Entity
from asset_loader import import_folder
import random

class Enemy(Entity):
    def __init__(self, enemy_type, player, pos, groups, obstacle_sprites, difficulty_multiplier, level):
        super().__init__(groups)

        stats = enemy_data[enemy_type]
        self.player = player
        self.level = level

        # load stats
        self.health = stats['health'] * difficulty_multiplier
        self.max_health = self.health * difficulty_multiplier
        self.speed = stats['speed'] * difficulty_multiplier
        self.damage = stats['damage'] * difficulty_multiplier
        
        self.notice_radius = stats['notice_radius']
        self.attack_radius = stats['attack_radius']
        self.attack_cooldown = stats['attack_cooldown']
        self.last_attack = 0
        self.exp_gain = stats['exp_gain']

        # animation setup
        self.image_path = stats['image_path'] 
        self.animations = self.load_animations(self.image_path)
        self.status = 'down_idle'
        self.image = pygame.image.load("../graphics/enemies/zombie/down_idle/idle_00.png")

        # rect + hitbox
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(0, -10)

        # patrol attributes
        self.wander_timer = 0
        self.wander_cooldown = 250
        self.direction = pygame.math.Vector2()
        self.facing_direction = 'down'


        self.obstacle_sprites = obstacle_sprites
        self.enemy_type = enemy_type
        self.behaviour = 'roam'

        self.loot_dropped = False

    def load_animations(self, base_path):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': [],
            'up_death': [], 'down_death': [], 'left_death': [], 'right_death': []
        }

        for animation in self.animations.keys():
            full_path = f"{base_path}/{animation}"
            self.animations[animation] = import_folder(full_path)
        return self.animations

    def pick_rand_direction(self):
        x = random.randint(-1,1)
        y = random.randint(-1,1)
        
        while x==0 and y==0:
             x = random.randint(-1,1)
             y = random.randint(-1,1)

        self.direction = pygame.math.Vector2(x,y)
    
    def get_status(self):
        if self.health <= 0:
            if not 'death' in self.status:
                self.frame_index =0
                self.status = self.facing_direction + '_death'
            return

        if 'attack' in self.status:
            return
        
        if self.direction.x > 0:
            self.facing_direction = 'right'
            self.status = 'right'

        elif self.direction.x < 0:
            self.facing_direction = 'left'
            self.status = 'left'

        elif self.direction.y > 0:
            self.facing_direction = 'down'
            self.status = 'down'

        elif self.direction.y < 0:
            self.facing_direction = 'up'
            self.status = 'up'

        # idle
        else:
            self.status = self.facing_direction + '_idle'
        
    def get_behaviour(self, player):
        player_pos =  pygame.math.Vector2(player.rect.center)
        enemy_pos = pygame.math.Vector2(self.rect.center)

        distance_from_player = (player_pos - enemy_pos).length()

        if distance_from_player <= self.attack_radius:
            self.behaviour = 'attack'
        elif distance_from_player <= self.notice_radius and distance_from_player > self.attack_radius:
            self.behaviour = 'chase'
        else:
             self.behaviour ='roam'


    def actions(self, player):
        current_time = pygame.time.get_ticks()

        if self.behaviour == 'attack':
            self.direction = pygame.math.Vector2()
            if current_time - self.last_attack >= self.attack_cooldown:
                self.status = self.facing_direction + '_attack'
                self.last_attack = current_time

                if self.rect.colliderect(player.hitbox):
                    player.take_damage(self.damage)

        elif self.behaviour == 'chase':
            self.chase(player)

        else:
            pass


    def chase(self, player):
        
        enemy_pos = pygame.math.Vector2(self.rect.center)
        player_pos = pygame.math.Vector2(player.rect.center)

        direction = player_pos - enemy_pos

        if direction.length() != 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.math.Vector2()


    def animate(self):
        animation = self.animations[self.status]

        if 'attack' in self.status:
            self.frame_index += self.animation_speed
            
            if self.frame_index >= len(animation):
            # if attack animation finished
                self.attacking = False
                self.frame_index = 0
                self.status = self.facing_direction + '_idle'
        
        elif 'death' in self.status:
            self.frame_index += self.animation_speed * 1.6
            
            if self.frame_index >= len(animation):
                self.alive = False
                self.kill()
                return

        else:
            # loop over the frame index
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):  # loop frames back to the beginning of the animation
                self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        if self.flash_timer > 0:
            alpha = 20 + int((self.flash_timer / self.flash_duration) * 400)
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(center=self.hitbox.center)  # keep rect centered on hitbox

    def take_damage(self, damage, attacker_pos):
        self.health -= damage
        self.flash_timer = self.flash_duration

        direction = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(attacker_pos)
        if direction.length != 0:
            direction = direction.normalize()

        knockback_strength = 30
        self.hitbox.centerx += direction.x * knockback_strength
        self.hitbox.centery += direction.y * knockback_strength
        self.rect.center = self.hitbox.center

        if self.health<=0:
            self.player.add_exp(self.exp_gain)

    def draw_health_bar(self, surface, offset):
        if self.health < self.max_health:  # only show when damaged
            bar_width = 40
            bar_height = 6
            fill = (self.health / self.max_health) * bar_width

            # bar position (above the enemy)
            x = self.hitbox.centerx - bar_width // 2
            y = self.hitbox.top - 30

            # subtract camera offset
            x -= offset.x   
            y -= offset.y

            # background bar
            pygame.draw.rect(surface, (60, 60, 60), (x, y, bar_width, bar_height))
            # fill with current health
            pygame.draw.rect(surface, (200, 0, 0), (x, y, fill, bar_height))


    def update(self, player):
        # death handling
        if self.health <= 0:
            if not self.loot_dropped:
                self.level.drop_loot()
                self.loot_dropped = True

            self.direction.update(0, 0)
            self.get_status()
            self.animate()
            return

        # alive behaviour 
        if self.flash_timer > 0:
            self.flash_timer -= 1

        self.wander_timer += 1
        if self.wander_timer >= self.wander_cooldown:
            self.pick_rand_direction()
            self.wander_timer = 0

        self.get_behaviour(player)
        self.actions(player)
        self.move(self.speed)
        self.get_status()
        self.animate()

