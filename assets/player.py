import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        
        # Carga y escala de la imagen
        original_image = pygame.image.load("assets/images/luz.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (80, 80))

        self.rect = self.image.get_rect(topleft=pos)
        self.speed = PLAYER_SPEED


        # Cargar sonido de impacto
        self.sonido_impacto = pygame.mixer.Sound("assets/sounds/impacto.wav")
        self.sonido_impacto.set_volume(0.5)  # Ajustar volumen

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Limitar el movimiento dentro de la pantalla
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
   


    def colisionar(self, obstaculos, level):
        for obstaculo in obstaculos:
            if self.rect.colliderect(obstaculo.rect):
                level.perder_fragmento()
                self.sonido_impacto.play()
                # Calculamos dirección del impacto
                dx = self.rect.centerx - obstaculo.rect.centerx
                dy = self.rect.centery - obstaculo.rect.centery
            
            # Definir una pequeña fuerza de empuje
                fuerza = 3
            
            # Empujar según dirección del impacto
                if dx > 0:  # Luz a la derecha del obstáculo
                    self.rect.x += fuerza
                else:  # Luz a la izquierda del obstáculo
                    self.rect.x -= fuerza
            
                if dy > 0:  # Luz está abajo del obstáculo
                    self.rect.y += fuerza
                else:  # Luz está arriba del obstáculo
                    self.rect.y -= fuerza
