import pygame
from player import Player
from fragment import FragmentoVoz
from obstacle import Obstaculo
from settings import *

    

class Level:
    

    
    def __init__(self):

        self.sonido_recolectar = pygame.mixer.Sound("assets/sounds/recolectar.wav")
        self.sonido_recolectar.set_volume(0.5)  # Ajusta el volumen
    
        self.mensajes = [
        "No estás sola.",
        "Tu voz importa.",
        "Esto también pasará.",
        "Eres suficiente.",
        "Hablar ayuda.",
        "Sigue adelante.",
        "Hay luz en ti."
    ]
        self.mensaje_actual = ""
        self.tiempo_mensaje = 0  # Tiempo en milisegundos

        # Cargar fondo escalado desde archivo correcto
        self.fondo_gris = pygame.image.load("assets/images/fondo_gris_800x600.png").convert()
        self.fondo_brillante = pygame.image.load("assets/images/fondo_brillante_800x600.png").convert()
        self.fondo_actual = self.fondo_gris.copy()
        self.player = Player((100, 100))

        
        self.player_group = pygame.sprite.GroupSingle(self.player)

        self.boton_reinicio = pygame.Rect(300, 500, 200, 50)

        
        
       
       
        
        # Crear fragmentos de voz
        try:
            with open("progreso.txt", "r") as archivo:
                datos = archivo.readline()
                fragmentos_guardados = int(datos.split(": ")[1])
                self.fragmentos_recogidos = min(fragmentos_guardados, NUM_FRAGMENTOS_NECESARIOS - 1)  # No permitir que inicie en estado final
        except FileNotFoundError:
                self.fragmentos_recogidos = 0  # Iniciar en cero si no hay datos guardados

        
        self.fragmentos_recogidos = 0
        self.juego_terminado = False
        # En level.py dentro de __init__
        self.fragmentos = pygame.sprite.Group()
        self.fragmento_posiciones = [
            (280, 380),   # cerca de esquina superior
            (30, 570),  # detrás de un elemento
            (620, 180),   # muy abajo
            (420, 320),  # zona media alejada
            (200, 250),  # esquina lejana
            (780, 20),  # casi fuera de foco
            (350, 520),  # al pasar una zona confusa
            (100, 48),  # escondido cerca del inicio
            (90,110),  # cerca de obstáculos futuros
            (700, 500),  # final del mapa
        ]
        for pos in self.fragmento_posiciones:
            self.fragmentos.add(FragmentoVoz(pos))
            # DEPURACIÓN: Ver colisiones entre fragmentos y obstáculos
            
        self.mensaje_final = "Gracias por seguir. La luz siempre vuelve."
        self.mostrar_mensaje_final = False

        self.obstaculos = pygame.sprite.Group()
        obstaculo_data = [
            ((200, 150), (80, 80), (2, 0)),  # Se mueve horizontalmente
            ((400, 300), (50, 150), (0, 2)),  # Se mueve verticalmente
            ((600, 100), (80, 80), (1, 1)),  # Se mueve diagonalmente
        ]

        for pos, size, speed in obstaculo_data:
            self.obstaculos.add(Obstaculo(pos, size, speed))

        

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.player.colisionar(self.obstaculos, self)
        
        for obstaculo in self.obstaculos: 
            self.obstaculos.update(self.fragmentos_recogidos)



        # Recolectar fragmentos
        recogidos = pygame.sprite.spritecollide(self.player, self.fragmentos, dokill=True)
        
        if recogidos:
            self.sonido_recolectar.play()
        # Muestra el mensaje correspondiente al fragmento recogido
            indice = min(self.fragmentos_recogidos - 1, len(self.mensajes) - 1)
            self.mensaje_actual = self.mensajes[indice]
            self.tiempo_mensaje = pygame.time.get_ticks()  # Guardamos el tiempo actual
        self.fragmentos.update()
        self.fragmentos_recogidos += len(recogidos)
         # Actualiza fondo con cada fragmento recogido
        self.guardar_progreso()  # Guarda el progreso en un archivo

        self.actualizar_fondo_transicion()

        # Cambiar a fondo brillante si se recolectaron suficientes fragmentos
        if self.fragmentos_recogidos >= NUM_FRAGMENTOS_NECESARIOS and not self.juego_terminado:
            self.fondo = pygame.image.load("assets/images/fondo_brillante_800x600.png").convert()
            self.juego_terminado = True
            self.mostrar_mensaje_final = True
            self.obstaculos.empty()
    def perder_fragmento(self):
        """Reduce los fragmentos y los hace reaparecer en su posición inicial"""
        if self.fragmentos_recogidos > 0:
            # Determinar la posición ANTES de reducir fragmentos
            nueva_pos = self.fragmento_posiciones[self.fragmentos_recogidos - 1]
        
        # Reducir fragmentos
            self.fragmentos_recogidos -= 1

        # Regenerar fragmento perdido
            self.fragmentos.add(FragmentoVoz(nueva_pos))


    def draw(self, screen):
        screen.blit(self.fondo_actual, (0, 0))
        self.fragmentos.draw(screen)
        self.obstaculos.draw(screen)

        self.player_group.draw(screen)
        self.dibujar_barra_progreso(screen)

        # Mostrar mensaje si no ha pasado más de 3 segundos (3000 ms)
        if self.mensaje_actual:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_mensaje < 3000:
                fuente = pygame.font.SysFont("Arial", 24)
                texto = fuente.render(self.mensaje_actual, True, (255, 255, 255))
                screen.blit(texto, (SCREEN_WIDTH // 2 - texto.get_width() // 2, 60))
            else:
                self.mensaje_actual = ""
        if self.mostrar_mensaje_final:
            font = pygame.font.SysFont(None, 48)
            text = font.render(self.mensaje_final, True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)


    
        print(f"Fragmentos en pantalla: {len(self.fragmentos.sprites())}")
        if self.juego_terminado:
            pygame.draw.rect(screen, (50, 150, 255), self.boton_reinicio)  # Dibujar botón azul
            font = pygame.font.SysFont(None, 36)
            texto = font.render("Reiniciar", True, (255, 255, 255))
            screen.blit(texto, (self.boton_reinicio.x + 60, self.boton_reinicio.y + 15))


    def dibujar_barra_progreso(self, screen):
    # Tamaño y posición de la barra
        barra_ancho = 200
        barra_alto = 20
        x = 20
        y = 20

        # Progreso
        progreso = self.fragmentos_recogidos / NUM_FRAGMENTOS_NECESARIOS
        ancho_relleno = int(barra_ancho * progreso)

        # Dibujar barra de fondo
        pygame.draw.rect(screen, (80, 80, 80), (x, y, barra_ancho, barra_alto))
        # Dibujar barra rellena
        pygame.draw.rect(screen, (255, 255, 100), (x, y, ancho_relleno, barra_alto))
        # Borde
        pygame.draw.rect(screen, (255, 255, 255), (x, y, barra_ancho, barra_alto), 2)

    def actualizar_fondo_transicion(self):
        progreso = self.fragmentos_recogidos / NUM_FRAGMENTOS_NECESARIOS
        self.fondo_actual = self.fondo_gris.copy()
    
        # Crea una copia del fondo brillante con transparencia
        brillante = self.fondo_brillante.copy()
        alpha = int(progreso * 255)  # entre 0 y 255
        brillante.set_alpha(alpha)
    
        # Superpone el brillante sobre el gris
        self.fondo_actual.blit(brillante, (0, 0))

    def guardar_progreso(self):
        """Guarda el número de fragmentos recolectados en un archivo plano"""
        with open("progreso.txt", "w") as archivo:
            archivo.write(f"Fragmentos recolectados: {self.fragmentos_recogidos}\n")

    def reiniciar_juego(self):
        """Reinicia todos los valores del juego para volver a jugar desde cero"""
        self.fragmentos_recogidos = 0
        self.juego_terminado = False
        self.mostrar_mensaje_final = False
        self.fondo_actual = self.fondo_gris.copy()

        # Restaurar fragmentos y obstáculos
        self.fragmentos.empty()
        for pos in self.fragmento_posiciones:
            self.fragmentos.add(FragmentoVoz(pos))

        self.obstaculos.empty()
        obstaculo_data = [
            ((200, 150), (80, 80), (2, 0)),
            ((400, 300), (50, 150), (0, 2)),
            ((600, 100), (80, 80), (1, 1))
        ]
        for pos, size, speed in obstaculo_data:
            self.obstaculos.add(Obstaculo(pos, size, speed))

    # Reiniciar posición del jugador
        self.player.rect.topleft = (100, 100)
