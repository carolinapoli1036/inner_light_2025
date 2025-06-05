import pygame

class FragmentoVoz(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Cargamos la imagen original
        original_image = pygame.image.load("assets/images/fragmento_voz.png").convert_alpha()

        # Escalamos la imagen a un tamaño más pequeño (por ejemplo, )
        self.original_image = pygame.transform.scale(original_image, (20, 20))

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(topleft=pos)

        

        # Variables para el efecto de brillo (parpadeo)
        self.alpha = 255
        self.alpha_direction = -5

    def update(self):
      
        # Cambiar opacidad para crear efecto de parpadeo
        self.alpha += self.alpha_direction

        
        if self.alpha <= 100 or self.alpha >= 255:
            self.alpha_direction *= -1

        self.image = self.original_image.copy()
        self.image.set_alpha(self.alpha)
