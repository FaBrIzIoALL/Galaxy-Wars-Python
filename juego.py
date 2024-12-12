import pygame
import random
import math
import os
import sys
from pygame import mixer

# Función para obtener rutas relativas (compatible con PyInstaller)
def ruta_relativa(ruta):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, ruta)
    return os.path.join(os.path.abspath("."), ruta)

# Inicializar Pygame
pygame.init()

# Música de fondo
mixer.music.load(ruta_relativa("MusicaFondo.mp3"))
mixer.music.set_volume(0.5)
mixer.music.play(-1)

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))

# Título e icono
pygame.display.set_caption("GalaxyWar")
icono = pygame.image.load(ruta_relativa("astronave.png"))
pygame.display.set_icon(icono)

# Texto final de juego
fuente_final = pygame.font.Font(ruta_relativa('CFGrandNord-Regular.ttf'), 80)

def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    texto_rect = mi_fuente_final.get_rect(center=(ANCHO // 2, ALTO // 2))
    pantalla.blit(mi_fuente_final, texto_rect.topleft)

# Fondo
fondo = pygame.image.load(ruta_relativa('fondo.jpg'))

# Jugador
img_jugador = pygame.image.load(ruta_relativa("nave-espacial.png"))
jugador_x = ANCHO // 2 - 32
jugador_y = ALTO - 100
jugador_x_cambio = 0

# Enemigos
CANTIDAD_ENEMIGOS = 9
img_enemigo = [pygame.image.load(ruta_relativa("ovni.png")) for _ in range(CANTIDAD_ENEMIGOS)]
enemigo_x = [random.randint(0, ANCHO - 64) for _ in range(CANTIDAD_ENEMIGOS)]
enemigo_y = [random.randint(50, 200) for _ in range(CANTIDAD_ENEMIGOS)]
enemigo_x_cambio = [0.3 for _ in range(CANTIDAD_ENEMIGOS)]
enemigo_y_cambio = [50 for _ in range(CANTIDAD_ENEMIGOS)]

# Balas
balas = []
img_bala = pygame.image.load(ruta_relativa("bala.png"))

# Puntaje
puntaje = 0
fuente = pygame.font.Font(None, 36)

# Funciones
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def enemigo(x, y, i):
    pantalla.blit(img_enemigo[i], (x, y))

def hay_colision(x1, y1, x2, y2):
    distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distancia < 27

# Bucle principal del juego
se_ejecuta = True
juego_terminado = False

while se_ejecuta:
    pantalla.blit(fondo, (0, 0))

    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Movimiento del jugador
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.5
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.5
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound(ruta_relativa("disparo.mp3"))
                sonido_bala.play()
                nueva_bala = {"x": jugador_x, "y": jugador_y, "velocidad": -5}
                balas.append(nueva_bala)

        if evento.type == pygame.KEYUP:
            if evento.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                jugador_x_cambio = 0

    if not juego_terminado:
        # Actualización del jugador
        jugador_x += jugador_x_cambio
        jugador_x = max(0, min(jugador_x, ANCHO - 64))

        # Actualización de enemigos
        for i in range(CANTIDAD_ENEMIGOS):
            enemigo_x[i] += enemigo_x_cambio[i]

            # Cambiar dirección en los bordes
            if enemigo_x[i] <= 0 or enemigo_x[i] >= ANCHO - 64:
                enemigo_x_cambio[i] *= -1
                enemigo_y[i] += enemigo_y_cambio[i]

            # Fin del juego si un enemigo llega a la base
            if enemigo_y[i] > ALTO - 150:
                juego_terminado = True
                balas.clear()

            # Colisiones con balas
            for bala in balas:
                if hay_colision(enemigo_x[i], enemigo_y[i], bala["x"], bala["y"]):
                    sonido_colision = mixer.Sound(ruta_relativa("golpe.mp3"))
                    sonido_colision.play()
                    balas.remove(bala)
                    puntaje += 1
                    enemigo_x[i] = random.randint(0, ANCHO - 64)
                    enemigo_y[i] = random.randint(50, 200)
                    break

            # Dibujar enemigos
            enemigo(enemigo_x[i], enemigo_y[i], i)

        # Movimiento de las balas
        for bala in balas[:]:
            bala["y"] += bala["velocidad"]
            pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
            if bala["y"] < 0:
                balas.remove(bala)

        # Dibujar jugador y puntaje
        jugador(jugador_x, jugador_y)
        mostrar_puntaje(10, 10)

    else:
        texto_final()

    pygame.display.update()

pygame.quit()
