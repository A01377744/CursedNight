import pygame
from random import randint
from math import sin

ANCHO = 800
ALTO = 600

BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
NEGRO = (1, 1, 1)

# Personaje
animacionCorrer = {0: (400, 900, 80, 118), 1: (480, 900, 90, 118), 2: (570, 900, 110, 118),
                   3: (680, 900, 110, 118), 4: (790, 900, 110, 118), 5: (900, 900, 110, 118), 6: (1010, 900, 110, 118)}
animacionAtaque = {0: (0, 460, 102, 120), 1: (102, 460, 90, 120), 2: (186, 460, 126, 115),
                   3: (310, 460, 126, 115), 4: (431, 460, 230, 120), 5: (660, 460, 230, 120)}
animacionSalto = {0: (430, 230, 70, 120), 1: (500, 230, 70, 120), 2: (571, 230, 70, 120),
                  3: (641, 230, 70, 120), 4: (712, 230, 75, 122), 5: (790, 230, 75, 122)}
QUIETO = 1
ABAJO = 2
ARRIBA = 6
SALTO = 3
CORRIENDO = 4
ATTACK = 5
PUNTOS = {1: 0}

# Enemigos
esqueleto = {0: (200, 0, 60, 110), 1: (260, 0, 60, 110)}
medusa = {0: (0, 0, 75, 75), 1: (75, 0, 75, 75), 2: (150, 0, 75, 75), 3: (225, 0, 70, 75)}
numeroDeEnemigos = 3
numeroDeMedusas = 2

TITULO = 0
MENU = 1
JUGANDO = 2
MUERTO = 3
GANADOR = 4
SCORE = 5


def dibujarPersonaje(ventana, frame, alturaPersonaje, accion, moviendo, listaEnemigos, spriteLatigo, alturaLatigo, listaMedusa):
    imgPersonaje = pygame.image.load('13974.gif')
    salto = None
    nuevaAccion = accion
    if accion == CORRIENDO:
        correr = frame % 7
        imgPersonaje.set_clip(pygame.Rect(animacionCorrer[correr]))
        imgPersonaje = imgPersonaje.subsurface(imgPersonaje.get_clip())
        x = 0
        if correr == 0:
            x += 30
        elif correr == 1:
            x += 20
        ventana.blit(imgPersonaje, (x, alturaPersonaje-116))
    elif accion == SALTO and moviendo == ARRIBA:
        if alturaPersonaje > 470:
            salto = 0
        elif alturaPersonaje > 450:
            salto = 1
        elif alturaPersonaje > 200:
            salto = 2
        imgPersonaje.set_clip(pygame.Rect(animacionSalto[salto]))
        imgPersonaje = imgPersonaje.subsurface(imgPersonaje.get_clip())
        ventana.blit(imgPersonaje, (50, alturaPersonaje - 116))
    elif accion == SALTO and moviendo == ABAJO:
        if alturaPersonaje > 470:
            salto = 3
        elif alturaPersonaje > 450:
            salto = 4
        elif alturaPersonaje > 200:
            salto = 5
        imgPersonaje.set_clip(pygame.Rect(animacionSalto[salto]))
        imgPersonaje = imgPersonaje.subsurface(imgPersonaje.get_clip())
        ventana.blit(imgPersonaje, (50, alturaPersonaje - 116))
    elif accion == ATTACK:
        ataque = frame % 7
        if ataque != 6:
            imgPersonaje.set_clip(pygame.Rect(animacionAtaque[ataque]))
            imgPersonaje = imgPersonaje.subsurface(imgPersonaje.get_clip())
            if ataque == 4 or ataque == 5:
                verificarAtaque(listaEnemigos, listaMedusa, spriteLatigo, alturaLatigo)
            ventana.blit(imgPersonaje, (50, alturaPersonaje-116))

        else:
            imgPersonaje.set_clip(pygame.Rect(animacionAtaque[0]))
            imgPersonaje = imgPersonaje.subsurface(imgPersonaje.get_clip())
            ventana.blit(imgPersonaje, (50, alturaPersonaje - 116))
            if alturaPersonaje == 500:
                nuevaAccion = CORRIENDO
            else:
                nuevaAccion = SALTO
    return nuevaAccion


def dibujarEsqueleto(ventana, frame, listaEnemigos):
    imgEsqueleto = pygame.image.load('dracula-sprite-transparent-png-5.gif')
    correr = (frame//4) % 2
    imgEsqueleto.set_clip(pygame.Rect(esqueleto[correr]))
    imgEsqueleto = imgEsqueleto.subsurface(imgEsqueleto.get_clip())
    for enemigo in listaEnemigos:
        x = enemigo.rect.left
        ventana.blit(imgEsqueleto, (x, 390))


def dibujarMedusa(ventana, frame, listaMedusa):
    imgMedusa = pygame.image.load('CVHoD_MedusaHead.png')
    correr = (frame//4) % 4
    imgMedusa.set_clip(pygame.Rect(medusa[correr]))
    imgMedusa = imgMedusa.subsurface(imgMedusa.get_clip())
    for enemigo in listaMedusa:
        x = enemigo.rect.left
        y = enemigo.rect.bottom
        ventana.blit(imgMedusa, (x, y))


def moverEnemigos(listaEnemigos):
    for k in range(len(listaEnemigos)-1, -1, -1):
        enemigo = listaEnemigos[k]
        enemigo.rect.left -= 12
        if enemigo.rect.left < -100:
            enemigo.rect.left = randint(800, 1500)


def moverMedusa(listaMedusa, frame):
    for k in range(len(listaMedusa)-1, -1, -1):
        medusa = listaMedusa[k]
        medusa.rect.left -= 12
        medusa.rect.bottom += sin(frame)*20
        if medusa.rect.left < -100:
            medusa.rect.left = randint(800, 1500)
            medusa.rect.bottom = 320


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


def dibujarHUD(ventana, frame):
    pygame.font.init()
    fuente = pygame.font.Font(None, 50)
    player = fuente.render('Player', 1, BLANCO)
    score = fuente.render('Score', 1, BLANCO)
    puntillos = str(PUNTOS[1])
    puntuacion = fuente.render(puntillos, 1, BLANCO)
    time = str(20-(frame//20))
    tiempo = fuente.render(time, 1,  BLANCO)
    ventana.blit(player, (10, 10))
    ventana.blit(score, (10, 50))
    ventana.blit(tiempo, (700, 10))
    ventana.blit(puntuacion, (130, 50))
    if time == '0':
        return True


def checarSalud(ventana, spritePersonaje, listaEnemigos, listaVidas):
    dmg = pygame.mixer.Sound('Dmg.wav')
    dmg2 = pygame.mixer.Sound('Dmg2.wav')
    dmg3 = pygame.mixer.Sound('Dmg3.wav')
    dmg4 = pygame.mixer.Sound('Dmg4.wav')

    pygame.font.init()
    vidas = pygame.font.Font(None, 50)
    pygame.font.Font.set_bold(vidas, True)
    for k in range(len(listaEnemigos)-1, -1, -1):
        enemigo = listaEnemigos[k]
        xp, yp, ap, altp = spritePersonaje.rect
        xe, ye, ae, alte = enemigo.rect
        xp += ap
        yp -= 8
        if xp >= xe and xp <= xe + ae and yp+altp >= ye and yp <= ye+alte:
            if 'I' in listaVidas:
                listaVidas.remove('I')
                enemigo.rect.left = randint(800, 1500)
                dmgRandom = randint(1, 4)
                if dmgRandom == 1:
                    dmg.play()
                elif dmgRandom == 2:
                    dmg2.play()
                elif dmgRandom == 3:
                    dmg3.play()
                else:
                    dmg4.play()

            if 'I' not in listaVidas:
                return True
    x = 0
    for vida in listaVidas:
        life = vidas.render(vida, 1, ROJO)
        x += 12
        ventana.blit(life, (120 + x, 10))


def restart():
    listaVidas = ['I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I']
    time = 0
    frame = 0
    accion = CORRIENDO
    y = 500
    moviendo = QUIETO
    PUNTOS[1] = 0
    return time, frame, listaVidas, accion, y, moviendo


def verificarAtaque(listaEnemigos, listaMedusa, spriteLatigo, alturaLatigo):
    pygame.mixer.init()
    whip2 = pygame.mixer.Sound('Whip2.wav')
    whip3 = pygame.mixer.Sound('Whip3.wav')
    xL, yL, aL, altL = spriteLatigo.rect
    whipSound = randint(1, 2)
    for k in range(len(listaEnemigos)-1, -1, -1):
        enemigo = listaEnemigos[k]
        xE, yE, aE, altE = enemigo.rect
        if xL + aL >= xE and xL <= xE + aE and alturaLatigo + altL >= yE and alturaLatigo <= yE + altE:
            PUNTOS[1] += 75
            if whipSound == 1:
                whip2.play()
            elif whipSound == 2:
                whip3.play()
            enemigo.rect.left = (randint(800, 1500))

    for i in range(len(listaMedusa)-1, -1, -1):
            medusa = listaMedusa[i]
            xM, yM, aM, altM = medusa.rect
            if xL + aL >= xM and xL <= xM + aM and alturaLatigo + altL >= yM and alturaLatigo <= yM + altM:
                PUNTOS[1] += 100
                if whipSound == 1:
                    whip2.play()
                elif whipSound == 2:
                    whip3.play()
                medusa.rect.left = (randint(800, 1500))


def dibujar():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()
    termina = False

    # Pantalla de título
    imgLogo = pygame.image.load('Logo.png')

    # Imágenes menu
    imgProtagonista = pygame.image.load('Menu.png')
    imgCastle = pygame.image.load('Castle.png')

    # Imagenes final
    ending = pygame.image.load('theEnd.jpg')

    # Parametros personaje
    imgPersonaje = pygame.image.load('13974.gif')
    imgPersonaje.set_clip(pygame.Rect(680, 900, 110, 118))
    imgPersonaje = imgPersonaje.subsurface(imgPersonaje.get_clip())
    spritePersonaje = pygame.sprite.Sprite()
    spritePersonaje.image = imgPersonaje
    spritePersonaje.rect = imgPersonaje.get_rect()
    spritePersonaje.rect.left = 0
    spritePersonaje.rect.bottom = 500

    # Parametros látigo
    imgLatigo = pygame.image.load('13974.gif')
    imgLatigo.set_clip(pygame.Rect(770, 490, 120, 20))
    imgLatigo = imgLatigo.subsurface(imgLatigo.get_clip())
    spriteLatigo = pygame.sprite.Sprite()
    spriteLatigo.image = imgLatigo
    spriteLatigo.rect = imgLatigo.get_rect()
    spriteLatigo.rect.left = spritePersonaje.rect.left + 160

    # Parametros enemigos
    listaEnemigos = []
    imgEnemigos = pygame.image.load('dracula-sprite-transparent-png-5.gif')
    imgEnemigos.set_clip(pygame.Rect(esqueleto[0]))
    imgEnemigos = imgEnemigos.subsurface(imgEnemigos.get_clip())
    x = randint(800, 2000)
    for k in range(numeroDeEnemigos):
        spriteEnemigo = pygame.sprite.Sprite()
        spriteEnemigo.image = imgEnemigos
        spriteEnemigo.rect = imgEnemigos.get_rect()
        spriteEnemigo.rect.left = x
        spriteEnemigo.rect.bottom = 500
        listaEnemigos.append(spriteEnemigo)

    # Parametros medusa
    listaMedusa = []
    imgMedusa = pygame.image.load('CVHoD_MedusaHead.png')
    imgMedusa.set_clip(pygame.Rect(medusa[0]))
    imgMedusa = imgMedusa.subsurface(imgMedusa.get_clip())
    for k in range(numeroDeMedusas):
        spriteMedusa = pygame.sprite.Sprite()
        spriteMedusa.image = imgMedusa
        spriteMedusa.rect = imgMedusa.get_rect()
        spriteMedusa.rect.left = x
        spriteMedusa.rect.bottom = 320
        listaMedusa.append(spriteMedusa)

    # Set de fondo
    imgFondo = pygame.image.load('Castle.jpg')
    imgBosque1 = pygame.image.load('Bosque1.png')
    imgBosque2 = pygame.image.load('Bosque2.png')
    imgTexturas = pygame.image.load('textures.png')
    imgSuelo = pygame.image.load('Floor.jpg')
    imgTexturas.set_clip(pygame.Rect(197, 1, 32, 64))

    # Sonido
    pygame.mixer.init()
    pygame.mixer.music.load('captura.mp3')
    pygame.mixer.music.play(-1)
    death = pygame.mixer.Sound('DeathOfSimon.wav')

    whip = pygame.mixer.Sound('Whip.wav')
    hit = pygame.mixer.Sound('Start.wav')
    scream = pygame.mixer.Sound('Scream.wav')
    jump = pygame.mixer.Sound('Jump.wav')

    # Menu
    font = pygame.font.SysFont('comicsansms', 50)
    play = font.render('START', True, (BLANCO))
    highscores = font.render('HIGHSCORES', True, (BLANCO))
    xStart = 500
    yStart = 100
    xHighscores = 440
    yHighscores = 150

    # Muerto
    imgMuerte = pygame.image.load('Death.png')
    fuenteMuerte = pygame.font.SysFont('Baskerville', 80)
    hasMuerto = fuenteMuerte.render('YOU DIED', True, ROJO)
    retry = font.render('RETRY', True, BLANCO)
    xRetry = 345
    yRetry = 500
    quit = font.render('QUIT', True, BLANCO)
    xQuit = 360
    yQuit = 550
    fuenteFinal = pygame.font.Font(None, 35)
    final = fuenteFinal.render('''You've reached the castle, now it's time''', True, BLANCO)
    final2 = fuenteFinal.render('''to kill the monster that lives inside.''', True, BLANCO)

    # Settings
    moviendo = QUIETO
    xBosque1 = 0
    xBosque2 = 0
    xSuelo = 0

    frame = 0
    enemyFrame = 0
    time = 0
    tMuerte = 0
    tGanador = 0
    parpadeo = 0
    estado = TITULO
    accion = CORRIENDO
    listaVidas = []

    while not termina:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                termina = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    if spritePersonaje.rect.bottom == 500:
                        moviendo = ARRIBA
                        if estado == JUGANDO:
                            jump.play()
                        accion = SALTO
                elif evento.key == pygame.K_SPACE:
                    accion = ATTACK
                    if estado == JUGANDO:
                        whip.play()
                    elif estado == TITULO:
                        hit.play()

                    frame = 0
            elif evento.type == pygame.MOUSEBUTTONUP:
                xm, ym = pygame.mouse.get_pos()
                if xm >= xStart and xm <= xStart +115 and ym >= yStart and ym <= yStart + 30 and estado == MENU:
                    estado = JUGANDO
                    time, frame, listaVidas, accion, spritePersonaje.rect.bottom, moviendo = restart()
                    hit.play()
                    accion = CORRIENDO
                if xm >= xHighscores and xm <= xHighscores + 232 and ym >= yHighscores and ym <= yHighscores + 30 and estado == MENU:
                    estado = TITULO
                    hit.play()
                if xm >= xQuit and xm <= xQuit + 85 and ym >= yQuit and ym <= yQuit + 30 and estado == MUERTO:
                    estado = TITULO
                    pygame.mixer.music.play()
                    tMuerte = 0
                if xm >= xRetry and xm <= xRetry + 120 and ym >= yRetry and ym <= yRetry + 30 and estado == MUERTO:
                    estado = JUGANDO
                    time, frame, listaVidas, accion, spritePersonaje.rect.bottom, moviendo = restart()
                    tMuerte = 0
                    accion = CORRIENDO
                    pygame.mixer.music.play()

        ventana.fill(NEGRO)
        if estado == JUGANDO:
            if moviendo == ARRIBA:
                spritePersonaje.rect.bottom -= 20
                if spritePersonaje.rect.bottom < 300:
                    moviendo = ABAJO
            elif moviendo == ABAJO:
                if spritePersonaje.rect.bottom != 500:
                    spritePersonaje.rect.bottom += 20
                    if spritePersonaje.rect.bottom == 500:
                        accion = CORRIENDO

            ventana.blit(imgFondo, (250, 0))
            ventana.blit(imgBosque2, (xBosque2, 100))

            xBosque1 += 2
            xBosque2 -= 0.15
            xSuelo += 10
            frame += 1
            enemyFrame += 1
            time += 1
            alturaLatigo = spritePersonaje.rect.bottom - 86

            moverEnemigos(listaEnemigos)
            moverArboles(ventana, imgBosque1, xBosque1)
            dibujarSuelo(ventana, imgSuelo, xSuelo)
            dibujarEsqueleto(ventana, enemyFrame, listaEnemigos)
            alturaPersonaje = spritePersonaje.rect.bottom
            muerto = checarSalud(ventana, spritePersonaje, listaEnemigos, listaVidas)
            winner = dibujarHUD(ventana, time)
            moverMedusa(listaMedusa, enemyFrame)
            dibujarMedusa(ventana, enemyFrame, listaMedusa)
            accion = dibujarPersonaje(ventana, frame, alturaPersonaje, accion, moviendo,
                                      listaEnemigos, spriteLatigo, alturaLatigo, listaMedusa)

            if muerto is True:
                estado = MUERTO
                scream.play()
                death.play()
                pygame.mixer.music.stop()
            if winner is True:
                pygame.mixer.music.stop()
                estado = GANADOR

        elif estado == TITULO:
            pygame.draw.rect(ventana, (0, 0, 0), (0, 0, 800, 600))
            ventana.blit(imgLogo, (randint(185, 187), randint(167, 168)))
            fuente = pygame.font.Font(None, 50)
            parpadeo += 1
            start = fuente.render('PUSH SPACE', 1, (255, 255, 255))
            if parpadeo//10 % 2 == 0:
                ventana.blit(start, (310, 500))

            if accion == ATTACK:
                estado = MENU

        elif estado == MENU:
            accion = None
            x = randint(0, 150)
            pygame.draw.rect(ventana, (250, x, x), (0, 0, 800, 600))
            ventana.blit(imgCastle, (0, 0))
            ventana.blit(imgProtagonista, (350, randint(260, 261)))
            ventana.blit(play, (xStart, yStart))
            ventana.blit(highscores, (xHighscores, yHighscores))

        elif estado == MUERTO:
            tMuerte += 1
            if tMuerte > 50:
                x = randint(0, 150)
                pygame.draw.rect(ventana, (250, x, x), (0, 0, 800, 600))
                ventana.blit(imgMuerte, (0, 0))
            if tMuerte > 20:
                ventana.blit(hasMuerto, (280, 50))

            if tMuerte > 100:
                ventana.blit(quit, (xQuit, yQuit))
                ventana.blit(retry, (xRetry, yRetry))

        elif estado == GANADOR:
            frame += 1
            tGanador += 1
            if tGanador < 20 and tGanador % 2 == 0:
                pygame.draw.rect(ventana, BLANCO, (0, 0, 800, 600))
            if tGanador > 50:
                ventana.blit(ending, (152, 0))
                pygame.draw.rect(ventana, NEGRO, (0, 0, 450-tGanador, 600))
                pygame.draw.rect(ventana, NEGRO, (350+tGanador, 0, 400, 600))
            if tGanador > 310:
                pygame.draw.rect(ventana, (20, 20, 100), (160, 470, 480, 60))
                pygame.draw.rect(ventana, BLANCO, (160, 470, 480, 60), 2)
                ventana.blit(final, (170, 475))
                ventana.blit(final2, (170, 500))
            if tGanador > 500:
                estado = SCORE
                tGanador = 0
        elif estado == SCORE:
            tGanador += 1
            puntillos = str(PUNTOS[1])
            puntuacion = font.render(puntillos, 1, BLANCO)
            finalScore = font.render('Final Score', 1, BLANCO)
            gracias = font.render('THANKS FOR PLAYING!', 1, BLANCO)
            if tGanador > 20:
                ventana.blit(finalScore, (220, 250))
            if tGanador > 50:
                ventana.blit(puntuacion, (450, 250))
            if tGanador > 100:
                pass
            if tGanador > 150:
                if tGanador//10 % 2 == 0:
                    ventana.blit(gracias, (190, 500))
            if tGanador > 200:
                if accion == ATTACK:
                    estado = TITULO
                    accion = QUIETO
                    pygame.mixer.music.play(-1)

        pygame.display.flip()
        reloj.tick(40)

    pygame.quit()


dibujar()
