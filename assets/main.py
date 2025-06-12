import pygame
from settings import *
from level import Level

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("INNER LIGHT")
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/musica_fondo.wav")  # Carga la música
pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen (0.0 a 1.0)
pygame.mixer.music.play(-1)  # Reproduce la música en bucle


# Cargar fondo de inicio solo una vez
fondo_inicio = pygame.image.load("assets/images/fondo_inicio.png").convert()
fondo_inicio = pygame.transform.scale(fondo_inicio, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fuente para el texto de instrucciones
fuente = pygame.font.SysFont(None, 28)

# Estados
pantalla_inicio = True
level = Level()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if pantalla_inicio:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pantalla_inicio = False
        else:
            if level.juego_terminado and event.type == pygame.MOUSEBUTTONDOWN:
                if level.boton_reinicio.collidepoint(event.pos):
                    level.reiniciar_juego()

    # Dibujar
    if pantalla_inicio:
        screen.blit(fondo_inicio, (0, 0))
        texto = fuente.render("Presiona ENTER para comenzar", True, (200, 200, 200))
        
        screen.blit(texto, texto.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))
    else:
        level.update()
        level.draw(screen)
        
    if level.juego_terminado and event.type == pygame.MOUSEBUTTONDOWN:
        if level.boton_reinicio.collidepoint(event.pos):
            level.reiniciar_juego()
    
        

    

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
