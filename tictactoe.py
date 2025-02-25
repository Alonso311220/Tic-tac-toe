import pygame
import random

#creación de la ventana para interactuar
pygame.init() 
screen = pygame.display.set_mode((600,600))#tamaño de nuestra ventana
pygame.display.set_caption("Tic Tac Toe")#Título
#cargamos el background, la x y el círculo
import os
ruta = os.path.join(os.path.dirname(__file__), 'static', 'background.png')
fondo = pygame.image.load(ruta)

import os
ruta_circulo = os.path.join(os.path.dirname(__file__), 'static', 'circle.png')
circulo = pygame.image.load(ruta_circulo)

import os
ruta_x = os.path.join(os.path.dirname(__file__), 'static', 'x.png')
equis = pygame.image.load(ruta_x)




# Escalar imágenes
fondo = pygame.transform.scale(fondo, (600, 600))
circulo = pygame.transform.scale(circulo, (125, 125))
equis = pygame.transform.scale(equis, (125, 125))

# Coordenadas del tablero (4x4)
coordenadas = [[(j * 150, i * 150) for j in range(4)] for i in range(4)]

# Inicialización del tablero (4x4)
tablero = [['' for _ in range(4)] for _ in range(4)]

# Variables de control
turno = 'o'
game_over = False
clock = pygame.time.Clock()
modo_agente = None  # Ningún modo seleccionado por defecto

def mostrar_menu():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    opciones = ["1. Aleatorio (Fácil)", "2. Defensivo (Normal)", "3. Estratégico (Imposible)"]
    for i, opcion in enumerate(opciones):
        texto = font.render(opcion, True, (255, 255, 255))
        screen.blit(texto, (200, 200 + i * 50))
    pygame.display.update()

def verificar_ganador(tablero):
    # Verificar filas
    for i in range(4):
        for j in range(1):
            if tablero[i][j] == tablero[i][j+1] == tablero[i][j+2] == tablero[i][j+3] != '':
                return tablero[i][j]
    # Verificar columnas
    for j in range(4):
        for i in range(1):
            if tablero[i][j] == tablero[i+1][j] == tablero[i+2][j] == tablero[i+3][j] != '':
                return tablero[i][j]
    # Verificar diagonales (izquierda a derecha)
    for i in range(1):
        for j in range(1):
            if tablero[i][j] == tablero[i+1][j+1] == tablero[i+2][j+2] == tablero[i+3][j+3] != '':
                return tablero[i][j]
    # Verificar diagonales (derecha a izquierda)
    for i in range(1):
        for j in range(3, 4):
            if tablero[i][j] == tablero[i+1][j-1] == tablero[i+2][j-2] == tablero[i+3][j-3] != '':
                return tablero[i][j]
    # Verificar empate
    if all(tablero[i][j] != '' for i in range(4) for j in range(4)):
        return 'empate'
    return None

def movimiento_aleatorio():
    movimientos = [(i, j) for i in range(4) for j in range(4) if tablero[i][j] == '']
    return random.choice(movimientos) if movimientos else None

def movimiento_defensivo():
    # Prioriza bloquear al jugador
    for i in range(4):
        for j in range(4):
            if tablero[i][j] == '':
                tablero[i][j] = 'o'
                if verificar_ganador(tablero) == 'o':
                    tablero[i][j] = ''
                    return i, j
                tablero[i][j] = ''
    return movimiento_aleatorio()

def minimax(tablero, profundidad, es_maximizando, alpha=-float('inf'), beta=float('inf')):
    resultado = verificar_ganador(tablero)
    if resultado is not None or profundidad == 0:
        if resultado == 'x':
            return 1
        elif resultado == 'o':
            return -1
        else:
            return 0

    if es_maximizando:
        mejor_puntaje = -float('inf')
        for i in range(4):
            for j in range(4):
                if tablero[i][j] == '':
                    tablero[i][j] = 'x'
                    puntaje = minimax(tablero, profundidad - 1, False, alpha, beta)
                    tablero[i][j] = ''
                    mejor_puntaje = max(puntaje, mejor_puntaje)
                    alpha = max(alpha, mejor_puntaje)
                    if beta <= alpha:
                        break
        return mejor_puntaje
    else:
        mejor_puntaje = float('inf')
        for i in range(4):
            for j in range(4):
                if tablero[i][j] == '':
                    tablero[i][j] = 'o'
                    puntaje = minimax(tablero, profundidad - 1, True, alpha, beta)
                    tablero[i][j] = ''
                    mejor_puntaje = min(puntaje, mejor_puntaje)
                    beta = min(beta, mejor_puntaje)
                    if beta <= alpha:
                        break
        return mejor_puntaje

def movimiento_estrategico():
    # Prioriza ganar sobre cualquier otra acción
    for i in range(4):
        for j in range(4):
            if tablero[i][j] == '':
                tablero[i][j] = 'x'
                if verificar_ganador(tablero) == 'x':
                    tablero[i][j] = ''
                    return i, j
                tablero[i][j] = ''
    # Si no puede ganar en un movimiento, usa minimax
    mejor_puntaje = -float('inf')
    mejor_movimiento = None
    for i in range(4):
        for j in range(4):
            if tablero[i][j] == '':
                tablero[i][j] = 'x'
                puntaje = minimax(tablero, 3, False)  # Límite de profundidad = 3
                tablero[i][j] = ''
                if puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje
                    mejor_movimiento = (i, j)
    return mejor_movimiento

def mejor_movimiento():
    if modo_agente == 1:
        return movimiento_aleatorio()
    elif modo_agente == 2:
        return movimiento_defensivo()
    elif modo_agente == 3:
        return movimiento_estrategico()

# Menú principal
mostrando_menu = True
while mostrando_menu:
    mostrar_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                modo_agente = 1
                mostrando_menu = False
            elif event.key == pygame.K_2:
                modo_agente = 2
                mostrando_menu = False
            elif event.key == pygame.K_3:
                modo_agente = 3
                mostrando_menu = False

# Bucle principal del juego
while not game_over:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN and turno == 'o':
            x, y = pygame.mouse.get_pos()
            for i in range(4):
                for j in range(4):
                    if coordenadas[i][j][0] <= x <= coordenadas[i][j][0] + 150 and coordenadas[i][j][1] <= y <= coordenadas[i][j][1] + 150:
                        if tablero[i][j] == '':
                            tablero[i][j] = 'o'
                            turno = 'x'
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            tablero = [['' for _ in range(4)] for _ in range(4)]
            game_over = False
            turno = 'o'

    if turno == 'x' and not game_over:
        movimiento = mejor_movimiento()
        if movimiento:
            tablero[movimiento[0]][movimiento[1]] = 'x'
            turno = 'o'

    screen.blit(fondo, (0, 0))
    for i in range(4):
        for j in range(4):
            if tablero[i][j] == 'o':
                screen.blit(circulo, coordenadas[i][j])
            elif tablero[i][j] == 'x':
                screen.blit(equis, coordenadas[i][j])

    ganador = verificar_ganador(tablero)
    if ganador:
        print(f"¡El ganador es {ganador}!") if ganador != 'empate' else print("¡Es un empate!")
        game_over = True

    pygame.display.update()

pygame.quit()