import pygame
from asset_loader import import_folder   
from collider import Collider

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.animations = {}
        self.frame_index = 0
        self.animation_speed = 0.10
        self.collider = Collider()
        self.alive = True

        self.flash_timer = 0
        self.flash_duration = 8 # will flash for 8 frames
        self.flash_mode = 'damage'

        self.walk_sound = pygame.mixer.Sound('../audio/footsteps_sfx.mp3')
        self.walk_sound.set_volume(0.4)

    def load_animations(self, base_path):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
            'up_melee': [], 'down_melee': [], 'left_melee': [], 'right_melee': [],
            'up_shoot': [], 'down_shoot': [], 'left_shoot': [], 'right_shoot': []
        }

        for animation in self.animations.keys():
            full_path = f"{base_path}/{animation}"
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        if 'melee' in self.status or 'shoot' in self.status:
            self.frame_index += self.animation_speed * 1.6 # 0.16
            
            if self.frame_index >= len(animation) and 'melee' in self.status:
                # if attack animation finished
                self.frame_index = 0
                self.status = self.status.replace('_melee', '')

            elif self.frame_index >= len(animation) and 'shoot' in self.status:
                self.shooting = False
                self.frame_index = 0
                self.status = self.status.replace('_shoot','')
        
        else:
            # loop over the frame index
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):  # loop frames back to the beginning of the animation
                self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]

        # flash logic (damage flicker consumable solid white flash)
        if self.flash_timer > 0:

            if self.flash_mode == 'damage':
                # existing flicker behaviour
                alpha = 30 + int((self.flash_timer / self.flash_duration) * 255)
                self.image.set_alpha(alpha)

            elif self.flash_mode == 'consumable':
                # solid white flash
                white_image = self.image.copy()
                white_image.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
                self.image = white_image
                self.image.set_alpha(255)

        else:
            self.image.set_alpha(255)

        self.rect = self.image.get_rect(center=self.hitbox.center)  # keep rect centered on hitbox

    def move(self, speed):
        # normalise diagonal movement
        if self.direction.length() != 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.hitbox.x += self.direction.x * speed
        self.collider.collision(self, self.obstacle_sprites, 'x')

        # vertical movement
        self.hitbox.y += self.direction.y * speed
        self.collider.collision(self, self.obstacle_sprites, 'y')

        self.rect.center = self.hitbox.center
        #self.walk_sound.play()

    def take_damage(self, damage):
        self.flash_mode = 'damage'
        self.health -= damage
        self.flash_timer = self.flash_duration
        if self.health <= 0:
            self.defeat()

    def defeat(self):
        from player import Player
        if isinstance(self, Player):
            print("GAME OVER")
        else:
            return
        