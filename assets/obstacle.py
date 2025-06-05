import pygame
from settings import NUM_FRAGMENTOS_NECESARIOS
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, pos, size, speed):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill((80, 80, 80))
        self.rect = self.image.get_rect(topleft=pos)
        
        # Convertimos la velocidad a un Vector2 para evitar errores de tipo
        self.speed = pygame.math.Vector2(speed)

    def update(self, fragmentos_recogidos):
        """Modifica el obstáculo según el progreso"""
        self.rect.x += self.speed.x
        self.rect.y += self.speed.y

    # Disminuir la opacidad progresivamente
        if fragmentos_recogidos >= NUM_FRAGMENTOS_NECESARIOS // 2:
            alpha = max(255 - (fragmentos_recogidos * 10), 50)  # Se vuelve más transparente
            self.image.set_alpha(alpha)

    # Invertir dirección si toca los bordes de la pantalla
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed.x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed.y *= -1

