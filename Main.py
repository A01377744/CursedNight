import pygame, random
from pygame import *

ANCHO = 800
ALTO = 600

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL_OSCURO = (0, 0, 50)
NEGRO = (1, 1, 1)

estadoPersonaje = {0: (680, 900, 110, 118), 1: (660, 480, 230, 95), 2: (570, 230, 60, 120)}

TITULO = 0
MENU = 1
JUGANDO = 2

QUIETO = 1
ABAJO = 2
SALTO = 3
CORRIENDO = 4
ATTACK = 5


def dibujarEsqueleto(ventana, listaEnemigos):
    # VISITAR a cada elemento
    for enemigo in listaEnemigos:
        ventana.blit(enemigo.image, enemigo.rect)


def moverEnemigos(listaEnemigos):
    for enemigo in listaEnemigos:
        enemigo.rect.left -= 6


def dibujarSuelo(ventana, imgSuelo, xSuelo):
    for renglon in range(2):
        for columna in range(14):
            xUpdate = (64 * columna)-xSuelo
            while not xUpdate > -64:
                xUpdate = xUpdate + 864
            ventana.blit(imgSuelo, (xUpdate, 500+(64*renglon)))


def dibujarBarda(ventana, imgBarda, xSuelo):
    for columna in range(27):
        xUpdate = (32 * columna) - xSuelo
        while not xUpdate > -64:
            xUpdate = xUpdate + 864
        ventana.blit(imgBarda, (xUpdate, 456))


def moverArboles(ventana, imgBosque1, xBosque1):
    for columna in range(3):
        xUpdate = (400 * columna) - xBosque1
        while not xUpdate > -600:
            xUpdate = xUpdate + 1400
        ventana.blit(imgBosque1, (xUpdate, 240))


def dibujar():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()
    termina = False
    esqueleto = {-1: (200, 0, 60, 110), 1: (160, 0, 40, 65)}

    # Pantalla de título
    imgLogo = pygame.image.load('Logo.png')

    # Parametros personaje
    imgPersonaje = pygame.image.load('13974.gif')
    imgPersonaje.set_clip(pygame.Rect(estadoPersonaje[0]))
    imgPersonaje = imgPersonaje.subsurface(imgPersonaje.get_clip())
    spritePersonaje = pygame.sprite.Sprite()
    spritePersonaje.image = imgPersonaje
    spritePersonaje.rect = imgPersonaje.get_rect()
    spritePersonaje.rect.left = 0
    spritePersonaje.rect.bottom = 500

    # Parametros enemigos
    listaEnemigos = []
    imgEnemigos = pygame.image.load('dracula-sprite-transparent-png-5.gif')
    imgEnemigos.set_clip(pygame.Rect(esqueleto[-1]))
    imgEnemigos = imgEnemigos.subsurface(imgEnemigos.get_clip())
    for k in range(1):
        spriteEnemigo = pygame.sprite.Sprite()
        spriteEnemigo.image = imgEnemigos
        spriteEnemigo.rect = imgEnemigos.get_rect()
        spriteEnemigo.rect.left = random.randint(800, 1000)
        spriteEnemigo.rect.bottom = 500
        listaEnemigos.append(spriteEnemigo)

    # Set de fondo
    imgFondo = pygame.image.load('Castle.jpg')
    imgBosque1 = pygame.image.load('Bosque1.png')
    imgBosque2 = pygame.image.load('Bosque2.png')
    imgTexturas = pygame.image.load('textures.png')
    imgTexturas.set_clip(pygame.Rect(131, 231, 64, 65))
    imgSuelo = imgTexturas.subsurface(imgTexturas.get_clip())
    imgTexturas.set_clip(pygame.Rect(197, 1, 32, 64))
    imgBarda = imgTexturas.subsurface(imgTexturas.get_clip())

    moviendo = QUIETO
    xBosque1 = 0
    xBosque2 = 0
    xSuelo = 0

    frame = 0
    estado = TITULO
    accion = CORRIENDO

    # Input
    while not termina:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                termina = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    if spritePersonaje.rect.bottom == 500:
                        moviendo = SALTO
                elif evento.key == pygame.K_SPACE:
                        accion = ATTACK

            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_UP:
                    moviendo = ABAJO

        ventana.fill(NEGRO)
        if estado == JUGANDO:
            if moviendo == SALTO:
                spritePersonaje.rect.bottom -= 10
                if spritePersonaje.rect.bottom < 300:
                    moviendo = ABAJO
            elif moviendo == ABAJO:
                if spritePersonaje.rect.bottom != 500:
                    spritePersonaje.rect.bottom += 10
            elif accion == ATTACK:
                ventana.blit(spritePersonaje.image, spritePersonaje.rect)

            ventana.blit(imgFondo, (250, 0))
            ventana.blit(imgBosque2, (xBosque2, 100))

            xBosque1 += 1.5
            xBosque2 -= 0.2
            xSuelo += 5
            frame += 1
            moverEnemigos(listaEnemigos)
            moverArboles(ventana, imgBosque1, xBosque1)
            dibujarBarda(ventana, imgBarda, xSuelo)
            dibujarEsqueleto(ventana, listaEnemigos)
            dibujarSuelo(ventana, imgSuelo, xSuelo)
            ventana.blit(spritePersonaje.image, spritePersonaje.rect)
            pygame.draw.line(ventana, NEGRO, (0, 500), (800, 500), 2)
        if estado == TITULO:
            ventana.blit(imgLogo, (187, 167))
            if accion == ATTACK:
                estado = JUGANDO

        pygame.display.flip()
        reloj.tick(40)

    pygame.quit()


dibujar()
