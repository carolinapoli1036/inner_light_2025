import pygame
from settings import *
from level import Level

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("INNER LIGHT")
clock = pygame.time.Clock()

pantalla_inicio = True
level = Level()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pantalla_inicio and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            pantalla_inicio = False

    if pantalla_inicio:
        screen.fill((30, 30, 30))
        font = pygame.font.SysFont(None, 48)
        texto = font.render("INNER LIGHT", True, (255, 255, 255))
        instrucciones = pygame.font.SysFont(None, 28).render("Presiona ENTER para comenzar", True, (200, 200, 200))
        screen.blit(texto, texto.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 40)))
        screen.blit(instrucciones, instrucciones.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20)))
    else:

        level.update()
        level.draw(screen)
        

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
