import pygame
#creación de la ventana para interactuar
pygame.init() 
screen = pygame.display.set_mode((600,600))#tamaño de nuestra ventana
pygame.display.set_caption("Tic Tac Toe")#Título
#cargamos el background, la x y el círculo
fondo = pygame.image.load('static/background.png')
circulo = pygame.image.load('static/circle.png')
equis = pygame.image.load('static/x.png')
#modificamos el fondo acorde a nuestra ventana
fondo = pygame.transform.scale(fondo, (600,600))
circulo = pygame.transform.scale(circulo, (125,125))
equis = pygame.transform.scale(equis, (125,125))
# Coordenadas de cada celda (4x4)
coordenadas = [
    [(0, 0), (150, 0), (300, 0), (450, 0)],
    [(0, 150), (150, 150), (300, 150), (450, 150)],
    [(0, 300), (150, 300), (300, 300), (450, 300)],
    [(0, 450), (150, 450), (300, 450), (450, 450)]
]

# Matriz para la lógica del juego (4x4)
tablero = [
    ['', '', '', ''],
    ['', '', '', ''],
    ['', '', '', ''],
    ['', '', '', '']
]

# Turno inicial
turno = 'o'
game_over = False
clock = pygame.time.Clock()

# Función para verificar el ganador en un tablero de 4x4
def verificar_ganador(tablero):
    # Verificar filas
    for fila in tablero:
        if fila[0] == fila[1] == fila[2] == fila[3] != '':
            return fila[0]
    # Verificar columnas
    for col in range(4):
        if tablero[0][col] == tablero[1][col] == tablero[2][col] == tablero[3][col] != '':
            return tablero[0][col]
    # Verificar diagonales
    if tablero[0][0] == tablero[1][1] == tablero[2][2] == tablero[3][3] != '':
        return tablero[0][0]
    if tablero[0][3] == tablero[1][2] == tablero[2][1] == tablero[3][0] != '':
        return tablero[0][3]
    # Verificar empate
    if all(tablero[i][j] != '' for i in range(4) for j in range(4)):
        return 'empate'
    return None

# Bucle principal del juego
while not game_over:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = pygame.mouse.get_pos()
            # Determinar en qué celda se hizo clic
            for i in range(4):
                for j in range(4):
                    if (coordenadas[i][j][0] <= x <= coordenadas[i][j][0] + 150 and
                        coordenadas[i][j][1] <= y <= coordenadas[i][j][1] + 150):
                        if tablero[i][j] == '':
                            tablero[i][j] = turno
                            turno = 'x' if turno == 'o' else 'o'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reiniciar el juego al presionar 'R'
                tablero = [['', '', '', ''], ['', '', '', ''], ['', '', '', ''], ['', '', '', '']]
                game_over = False
                turno = 'o'

    # Dibujar el fondo
    screen.blit(fondo, (0, 0))

    # Dibujar las fichas en el tablero
    for i in range(4):
        for j in range(4):
            if tablero[i][j] == 'o':
                screen.blit(circulo, coordenadas[i][j])
            elif tablero[i][j] == 'x':
                screen.blit(equis, coordenadas[i][j])

    # Verificar si hay un ganador
    ganador = verificar_ganador(tablero)
    if ganador:
        print(f"¡El ganador es {ganador}!" if ganador != 'empate' else "¡Es un empate!")
        game_over = True

    # Actualizar la pantalla
    pygame.display.update()

# Salir de Pygame
pygame.quit()