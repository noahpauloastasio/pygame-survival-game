class Collider:
    def collision(self, entity, obstacles, axis):
        for tile in obstacles:
            if tile.hitbox.colliderect(entity.hitbox):

                if axis == 'x':
                    if entity.direction.x > 0:
                        entity.hitbox.right = tile.hitbox.left
                    else:
                        entity.hitbox.left = tile.hitbox.right

                else:  # axis == 'y'
                    if entity.direction.y > 0:
                        entity.hitbox.bottom = tile.hitbox.top
                    else:
                        entity.hitbox.top = tile.hitbox.bottom
