import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, damage, frames, attackable_sprites):
        super().__init__()
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 0.2

        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=pos)

        self.direction = direction
        self.speed = speed
        self.damage = damage

        self.attackable_sprites = attackable_sprites

        self.lifetime = 1000  # ms
        self.spawn_time = pygame.time.get_ticks()

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]
    
    def check_collision(self):
        hits = pygame.sprite.spritecollide(self, self.attackable_sprites, False)

        for enemy in hits:
            enemy.take_damage(self.damage, self.rect.center)
            self.kill()

    def update(self, *args):
        self.animate()

        self.rect.centerx += self.direction.x * self.speed 
        self.rect.centery += self.direction.y * self.speed

        self.check_collision()

        # lifetime
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
