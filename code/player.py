import pygame
from entity import Entity
from settings import *
from projectile import Projectile


class Player(Entity):
    def __init__(self, pos, groups,obstacle_sprites,attack_hitbox_sprites, attackable_sprites, visible_sprites, level):
        super().__init__(groups)
        self.image = pygame.image.load("../graphics/Player/down_idle/down_idle_0.png")

        self.rect = self.image.get_rect(topleft = pos)

        self.status = 'down'
        self.attacking = False

        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.attack_hitbox_sprites = attack_hitbox_sprites
        self.attackable_sprites = attackable_sprites
        self.visible_sprites = visible_sprites
        # collision rectangle (slightly smaller)
        self.hitbox = self.rect.inflate(0, -1) # shrink vertically for smoother movement

        self.stats = {'health': 100, 'energy':60, 'attack':10, 'speed': 5, 'level':0} # initiate the player with this. Actual current stats are stored in variables below
        self.current_max_stats = {'health': 100, 'energy':60, 'attack':10, 'speed': 5}
        self.max_stats = {'health': 300, 'energy':140, 'attack':20, 'speed': 10}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.attack = self.stats['attack']
        self.exp = 91
        self.exp_level = 0
        self.level=level
        self.exp_next_rank = 100
        self.speed = self.stats['speed']

        # inventory
        self.inventory = ['dagger', '', '', '', '']
        self.selected_index = 0
        self.equipped = self.inventory[self.selected_index]
        self.bullets = 10
        self.max_bullets = 99

        # combat
        self.attack_cooldown = 600
        self.remaining_attack_cooldown = 0
        self.ranged_cooldown = 1000
        self.last_ranged_attack = 0
        self.shooting = False

        self.load_animations("../graphics/Player")
        self.bullet_frames = {
            'up': import_folder('../graphics/gun_bullet/up_bullet'),
            'down': import_folder('../graphics/gun_bullet/down_bullet'),
            'left': import_folder('../graphics/gun_bullet/left_bullet'),
            'right': import_folder('../graphics/gun_bullet/right_bullet')
        }
        self.weapons = {'dagger': {'type': 'melee', 'damage': 10, 'cooldown': 250},
                      'pistol': {'type':'ranged', 'damage': 20, 'cooldown': 250, 'speed': 10, 'frames':self.bullet_frames},
                                 'health_potion': {'type': 'consumable', 'heal': 25}
        }
        
        self.consumables = {
            'soda': {'type': 'consumable', 'health': 0,  'energy': 15, 'speed': 1, 'attack': 0},
            'mre':  {'type': 'consumable', 'health': 25, 'energy': 20, 'speed': 0, 'attack': 0},
            'syringe': {'type': 'consumable', 'health': 100, 'energy':50, 'speed':3, 'attack': 3},
            'peas': {'type': 'consumable', 'health': 5,  'energy': 5,  'speed': 0, 'attack': 2},
            'bullets': {'type': 'consumables', 'amount':5}
        }



        # sound effects
        self.melee_sound = pygame.mixer.Sound('../audio/melee_sfx2.wav')
        self.pistol_sound = pygame.mixer.Sound('../audio/pistol_sfx2.wav') 
        self.melee_sound.set_volume(1)
        self.pistol_sound.set_volume(1)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'

        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'

        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'

        else:
            self.direction.x = 0

        # action input
        if keys[pygame.K_SPACE]:
                    item_name = self.inventory[self.selected_index]
                    
                    #if not self.equipped:
                    #    return
                    if item_name == '':
                        return
                    
                    if item_name in self.weapons:
                        item = self.weapons[item_name]

                        if item['type'] == 'melee':
                            self.melee_animation()
                        elif item['type'] == 'ranged':
                            self.ranged_attack()
                            self.pistol_sound.play()

                    elif item_name in self.consumables:
                            self.use_consumable(item_name)
               

        # selecting inventory slot
        if keys[pygame.K_1]:
            self.selected_index = 0
        elif keys[pygame.K_2]:
            self.selected_index = 1
        elif keys[pygame.K_3]:
            self.selected_index = 2
        elif keys[pygame.K_4]:
            self.selected_index = 3
        elif keys[pygame.K_5]:
            self.selected_index = 4
        
        item = self.inventory[self.selected_index]
        if item == '':
            self.equipped = None
        else:
            self.equipped = item

    def get_status(self):
        # ranged attack
        if self.shooting:
            self.direction.x = 0
            self.direction.y = 0
            
            if '_shoot' not in self.status:
                facing_direction = self.status.split('_')[0]
                self.status = facing_direction + '_shoot'
            return
            
        # idle 
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'melee' in self.status and not 'shoot' in self.status: # check status is not already idle, only add _idle once and not multiple times
                self.status = self.status + '_idle'
        # melee attack
        if self.attacking:
            self.direction.x = 0 # player can't move and attack at the same time
            self.direction.y = 0
            if not 'melee' in self.status:
                if 'idle' in self.status:
                    # overwrite idle
                    self.status = self.status.replace('_idle','_melee')
                else:
                    self.status = self.status + '_melee'

        else:

            if 'melee' in self.status:
                self.status = self.status.replace('_melee','')

            elif 'shoot' in self.status:
                self.status = self.status.replace('_shoot','')
        
    def add_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_next_rank:
            self.level_up()
            self.exp -=self.exp_next_rank

    def level_up(self):
        self.exp_level += 1
        self.upgrade_player()

    def upgrade_player(self):
        pass
        '''self.health = min(self.current_max_stats['health'] * 1.1, self.max_stats['health'])
        self.energy = min(self.current_max_stats['energy'] * 1.1, self.max_stats['energy'])
        self.attack = min(self.current_max_stats['attack'] * 1.1, self.max_stats['attack'])
        self.speed = min(self.current_max_stats['speed'] * 1.1, self.max_stats['speed'])'''

    def melee_animation(self):
        if not self.attacking:
            if self.use_energy(10):
                if pygame.time.get_ticks() >= self.remaining_attack_cooldown and self.equipped:
                    self.attacking = True
                    self.frame_index = 0

                    self.melee_sound.play()

                    self.remaining_attack_cooldown = pygame.time.get_ticks() + self.attack_cooldown
                    base = self.status.split('_')[0]
                    self.status = base + '_melee'
                    self.melee_attack_hitbox()
            else:
                pass

    def melee_attack_hitbox(self):
        # set where the hitbox should appear based on facing direction
        facing_direction = self.status.split('_')[0]

        if facing_direction == 'right':
            offset = pygame.math.Vector2(40, 0)
        elif facing_direction == 'left':
            offset = pygame.math.Vector2(-40, 0)
        elif facing_direction == 'up':
            offset = pygame.math.Vector2(0, -40)
        else:   # down
            offset = pygame.math.Vector2(0, 40)

        hitbox_pos = self.rect.center + offset

        # spawn the hitbox
        hitbox_rect = pygame.Rect(0, 0, 40, 40)
        hitbox_rect.center = hitbox_pos

        for enemy in self.attackable_sprites:
            if hitbox_rect.colliderect(enemy.hitbox):
                print('hit')
                enemy.take_damage(self.weapons[self.equipped]['damage'] + self.attack, self.rect.center)

        screen_rect = hitbox_rect.copy()
        screen_rect.topleft -= self.visible_sprites.offset 
        pygame.draw.rect(self.visible_sprites.display_surface, (255,0,0), screen_rect)

    def ranged_attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_ranged_attack < self.ranged_cooldown or not self.bullets > 0:
            return
        
        self.last_ranged_attack = current_time
        self.shooting = True
        self.bullets -= 1

        stats = self.weapons[self.equipped]

        facing_direction = self.status.split('_')[0]
        frames = stats['frames'][facing_direction]
        self.frame_index = 0

        self.pistol_sound.play()

        # spawn position 
        if 'up' in self.status:
            spawn_pos = self.rect.midtop
            direction = pygame.math.Vector2(0, -1)
        elif 'down' in self.status:
            spawn_pos = self.rect.midbottom
            direction = pygame.math.Vector2(0, 1)
        elif'left' in self.status:
            spawn_pos = self.rect.midleft
            direction = pygame.math.Vector2(-1, 0)
        elif 'right' in self.status:
            spawn_pos = self.rect.midright
            direction = pygame.math.Vector2(1, 0)

        # create projectile
        projectile = Projectile(
            spawn_pos,
            direction,
            stats['speed'],
            stats['damage'],
            frames,
            self.attackable_sprites
        )

        self.level.visible_sprites.add(projectile)

    def use_energy(self, amount):
        if self.energy - amount >= 0:
            self.energy -= amount
            self.melee_sound.play()
            return True
        else:
            return False
        
    def cooldown(self):
        if self.attacking:
            if pygame.time.get_ticks() >= self.remaining_attack_cooldown:
                self.attacking = False

    def regenerate_energy(self):
        regen_rate = 0.05  # energy recovered per frame
        max_energy = self.current_max_stats['energy']
        if self.energy < max_energy:
            self.energy += regen_rate
            if self.energy > max_energy:
                self.energy = max_energy

    def add_to_inventory(self, item):
        for slot in range(len(self.inventory)):
            if self.inventory[slot] == '':
                self.inventory[slot] = item
                return True

        # no empty slots found
        return False

    def use_consumable(self, item):
            self.health = min(self.health + self.consumables[item]['health'], self.current_max_stats['health'])
            self.energy = min(self.energy + self.consumables[item]['energy'], self.current_max_stats['energy'])
            self.speed = min(self.speed + self.consumables[item]['speed'], self.current_max_stats['speed'])
            self.attack = min(self.attack + self.consumables[item]['attack'], self.current_max_stats['attack'])

            self.flash_mode = 'consumable'
            self.flash_timer = self.flash_duration

            # remove the item from inventory
            for i in range(len(self.inventory)):
                if self.inventory[i] == item:
                    self.inventory[i] = ''
                    break


    def update(self, *args):
        if self.flash_timer > 0:
            self.flash_timer -= 1

        self.cooldown()
        self.regenerate_energy()
        self.input()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
