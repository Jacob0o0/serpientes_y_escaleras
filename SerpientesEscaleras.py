import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 600, 600
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Serpientes y Escaleras")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Preguntar al usuario cuántas celdas desea en el tablero
celdas = int(input("Ingrese el número de celdas por lado del tablero (Ej. 10 para un tablero 10x10): "))

# Validar entrada del usuario
if celdas < 2:
    print("El tablero debe tener al menos 2 celdas por lado. Usando 2x2 como valor mínimo.")
    celdas = 2

# Dimensiones del tablero
FILAS, COLUMNAS = celdas, celdas
TAMANIO_CASILLA = ANCHO // COLUMNAS

# Posiciones de las serpientes y escaleras
serpientes = {97: 78, 64: 60, 59: 19}
escaleras = {4: 14, 9: 31, 28: 84}

# Ajustar las serpientes y escaleras para que estén dentro del tamaño del tablero
serpientes = {inicio: fin for inicio, fin in serpientes.items() if inicio <= FILAS * COLUMNAS and fin <= FILAS * COLUMNAS}
escaleras = {inicio: fin for inicio, fin in escaleras.items() if inicio <= FILAS * COLUMNAS and fin <= FILAS * COLUMNAS}

# Función para convertir el número de casilla a coordenadas en la pantalla
def obtener_coordenadas(casilla):
    fila = (casilla - 1) // COLUMNAS
    if fila % 2 == 0:
        columna = (casilla - 1) % COLUMNAS
    else:
        columna = COLUMNAS - 1 - (casilla - 1) % COLUMNAS
    x = columna * TAMANIO_CASILLA
    y = (FILAS - 1 - fila) * TAMANIO_CASILLA
    return x, y

# Dibujar el tablero
def dibujar_tablero():
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            x = columna * TAMANIO_CASILLA
            y = fila * TAMANIO_CASILLA
            casilla = fila * COLUMNAS + (columna + 1) if fila % 2 == 0 else (fila + 1) * COLUMNAS - columna
            pygame.draw.rect(screen, BLANCO if casilla % 2 == 0 else NEGRO, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA))
            numero_texto = fuente.render(str(casilla), True, AZUL)
            screen.blit(numero_texto, (x + 5, y + 5))

# Dibujar serpientes y escaleras
def dibujar_serpientes_escaleras():
    for inicio, fin in serpientes.items():
        x1, y1 = obtener_coordenadas(inicio)
        x2, y2 = obtener_coordenadas(fin)
        pygame.draw.line(screen, ROJO, (x1 + TAMANIO_CASILLA // 2, y1 + TAMANIO_CASILLA // 2), (x2 + TAMANIO_CASILLA // 2, y2 + TAMANIO_CASILLA // 2), 5)

    for inicio, fin in escaleras.items():
        x1, y1 = obtener_coordenadas(inicio)
        x2, y2 = obtener_coordenadas(fin)
        pygame.draw.line(screen, VERDE, (x1 + TAMANIO_CASILLA // 2, y1 + TAMANIO_CASILLA // 2), (x2 + TAMANIO_CASILLA // 2, y2 + TAMANIO_CASILLA // 2), 5)

# Fuente para los números de casillas
fuente = pygame.font.SysFont("Arial", 18)

# Posición inicial del jugador
posicion_jugador = 1

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dibujar el fondo
    screen.fill(BLANCO)

    # Dibujar tablero, serpientes, escaleras y jugador
    dibujar_tablero()
    dibujar_serpientes_escaleras()

    # Dibujar jugador
    x_jugador, y_jugador = obtener_coordenadas(posicion_jugador)
    pygame.draw.circle(screen, AZUL, (x_jugador + TAMANIO_CASILLA // 2, y_jugador + TAMANIO_CASILLA // 2), 20)

    # Actualizar la pantalla
    pygame.display.flip()

    # Control básico para mover al jugador (solo para pruebas)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        if posicion_jugador < FILAS * COLUMNAS:
            posicion_jugador += 1
        pygame.time.delay(100)

    if keys[pygame.K_LEFT]:
        if posicion_jugador > 1:
            posicion_jugador -= 1
        pygame.time.delay(100)

    # Verificar si el jugador cae en una serpiente o sube por una escalera
    if posicion_jugador in serpientes:
        posicion_jugador = serpientes[posicion_jugador]
    elif posicion_jugador in escaleras:
        posicion_jugador = escaleras[posicion_jugador]