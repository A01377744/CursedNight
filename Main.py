import pygame, random
from pygame import *

ANCHO = 800
ALTO = 600

BLANCO = (255, 255, 255)
ROJO = (100, 0, 0)
AZUL_OSCURO = (0, 0, 50)
NEGRO = (1, 1, 1)

animacionCorrer = {0: (400, 900, 80, 118), 1: (480, 900, 90, 118), 2: (570, 900, 110, 118),
                   3: (680, 900, 110, 118), 4: (790, 900, 110, 118), 5: (900, 900, 110, 118), 6: (1010, 900, 110, 118)}
animacionAtaque = {0: (660, 480, 230, 95)}
animacionSalto = {0: (570, 230, 60, 120)}

TITULO = 0
MENU = 1
JUGANDO = 2

QUIETO = 1
ABAJO = 2
SALTO = 3
CORRIENDO = 4
ATTACK = 5


def dibujarPersonaje(ventana, actualizaciones, alturaPersonaje, accion):
    imgPersonaje = pygame.image.load('13974.gif')
    if accion == CORRIENDO:
        correr = actualizaciones % 7
        imgPersonaje.set_clip(pygame.Rect(animacionCorrer[correr]))
        imgPersonaje = imgPersonaje.subsurface(imgPersonaje.get_clip())
        ventana.blit(imgPersonaje, (0, alturaPersonaje-116))
    elif accion == SALTO:
        imgPersonaje.set_clip(pygame.Rect(animacionSalto[0]))
        imgPersonaje = imgPersonaje.subsurface(imgPersonaje.get_clip())
        ventana.blit(imgPersonaje, (0, alturaPersonaje - 116))


def dibujarEsqueleto(ventana, listaEnemigos):
    # VISITAR a cada elemento
    for enemigo in listaEnemigos:
        ventana.blit(enemigo.image, enemigo.rect)


def moverEnemigos(listaEnemigos):
    for k in range(len(listaEnemigos)-1, -1, -1):
        enemigo = listaEnemigos[k]
        enemigo.rect.left -= 11
        if enemigo.rect.left < -100:
            listaEnemigos.remove(enemigo)
            break


def dibujarSuelo(ventana, imgSuelo, xSuelo):
    for columna in range(2):
        xUpdate = (800 * columna)-xSuelo
        while not xUpdate > -800:
            xUpdate = xUpdate + 1600
        ventana.blit(imgSuelo, (xUpdate, 500))


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


def dibujarHUD(ventana):
    pygame.font.init()
    fuente = pygame.font.Font(None, 50)
    player = fuente.render('Player', 1, (255, 255, 255))
    enemy = fuente.render('Enemy', 1, (255, 255, 255))
    ventana.blit(player, (10, 10))
    ventana.blit(enemy, (10, 50))



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
    imgPersonaje.set_clip(pygame.Rect(680, 900, 110, 118))
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
    for k in range(20):
        spriteEnemigo = pygame.sprite.Sprite()
        spriteEnemigo.image = imgEnemigos
        spriteEnemigo.rect = imgEnemigos.get_rect()
        spriteEnemigo.rect.left = random.randint(800, 4000)
        spriteEnemigo.rect.bottom = 500
        listaEnemigos.append(spriteEnemigo)

    # Set de fondo
    imgFondo = pygame.image.load('Castle.jpg')
    imgBosque1 = pygame.image.load('Bosque1.png')
    imgBosque2 = pygame.image.load('Bosque2.png')
    imgTexturas = pygame.image.load('textures.png')
    imgSuelo = pygame.image.load('Floor.jpg')
    imgTexturas.set_clip(pygame.Rect(197, 1, 32, 64))
    imgBarda = imgTexturas.subsurface(imgTexturas.get_clip())

    moviendo = QUIETO
    xBosque1 = 0
    xBosque2 = 0
    xSuelo = 0

    frame = 0
    estado = TITULO
    actualizaciones = 1
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
                        accion = SALTO
                elif evento.key == pygame.K_SPACE:
                        accion = ATTACK

        ventana.fill(NEGRO)
        if estado == JUGANDO:
            if moviendo == SALTO:
                spritePersonaje.rect.bottom -= 10
                if spritePersonaje.rect.bottom < 300:
                    moviendo = ABAJO
            elif moviendo == ABAJO:
                if spritePersonaje.rect.bottom != 500:
                    spritePersonaje.rect.bottom += 10
                    if spritePersonaje.rect.bottom == 500:
                        accion = CORRIENDO
            ventana.blit(imgFondo, (250, 0))
            ventana.blit(imgBosque2, (xBosque2, 100))

            xBosque1 += 2
            xBosque2 -= 0.2
            xSuelo += 10
            frame += 1
            actualizaciones += 1
            moverEnemigos(listaEnemigos)
            moverArboles(ventana, imgBosque1, xBosque1)
            dibujarEsqueleto(ventana, listaEnemigos)
            dibujarSuelo(ventana, imgSuelo, xSuelo)
            pygame.draw.line(ventana, NEGRO, (0, 500), (800, 500), 2)
            alturaPersonaje = spritePersonaje.rect.bottom
            dibujarPersonaje(ventana, actualizaciones, alturaPersonaje, accion)
            dibujarHUD(ventana)
        if estado == TITULO:
            x = random.randint(0, 50)
            pygame.draw.rect(ventana, (x, x, x), (0, 0, 800, 600))
            ventana.blit(imgLogo, (187, 167))
            if accion == ATTACK:
                estado = JUGANDO
                accion = CORRIENDO

        pygame.display.flip()
        reloj.tick(40)

    pygame.quit()


dibujar()
