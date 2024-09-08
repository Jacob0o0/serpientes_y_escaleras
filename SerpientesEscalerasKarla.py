import pygame
import sys
import math
import random

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

# Preguntar al usuario el número total de celdas
total_celdas = int(input("Ingrese el número total de celdas para el tablero (Ej. 36 para un tablero 6x6): "))

# Validar la entrada del usuario
limite_maximo = 100  # Limite máximo de celdas
if total_celdas < 4:
    print("El tablero debe tener al menos 4 celdas. Usando 4 como valor mínimo.")
    total_celdas = 4
elif total_celdas > limite_maximo:
    print(f"El tablero no puede tener más de {limite_maximo} celdas. Usando {limite_maximo} como valor máximo.")
    total_celdas = limite_maximo

# Función para verificar si un número es primo
def es_primo(num):
    if num <= 1:
        return False
    if num <= 3:
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True

# Función para calcular las dimensiones más cercanas al cuadrado posible
def calcular_dimensiones(celdas):
    if es_primo(celdas) and celdas > 4:
        # Para números primos mayores a 4, usar una matriz cuadrada cercana
        lado = int(math.ceil(math.sqrt(celdas)))
        return lado, lado
    else:
        filas = int(math.sqrt(celdas))
        columnas = filas
        while filas * columnas < celdas:
            if columnas <= filas:
                columnas += 1
            else:
                filas += 1
        return filas, columnas

# Determinar las dimensiones del tablero
FILAS, COLUMNAS = calcular_dimensiones(total_celdas)

# Calcular el tamaño de cada celda basado en las dimensiones de la pantalla
TAMANIO_CASILLA = min(ANCHO // COLUMNAS, ALTO // FILAS)

# Función para obtener todas las celdas válidas en el tablero (no vacías)
def obtener_celdas_validas():
    celdas_validas = set(range(2, total_celdas + 1))  # Evitar la primera casilla
    return celdas_validas

# Función para obtener la fila y columna de una casilla
def obtener_fila_columna(casilla):
    fila = (casilla - 1) // COLUMNAS
    if fila % 2 == 0:
        columna = (casilla - 1) % COLUMNAS
    else:
        columna = COLUMNAS - 1 - (casilla - 1) % COLUMNAS
    return fila, columna

# Función para verificar si dos casillas están en la misma fila o columna
def son_misma_fila_columna(casilla1, casilla2):
    fila1, columna1 = obtener_fila_columna(casilla1)
    fila2, columna2 = obtener_fila_columna(casilla2)
    return fila1 == fila2 or columna1 == columna2

# Función para verificar si la diferencia entre dos casillas es de al menos 5 filas o columnas
def es_diferencia_adecuada(casilla1, casilla2):
    fila1, columna1 = obtener_fila_columna(casilla1)
    fila2, columna2 = obtener_fila_columna(casilla2)
    return abs(fila1 - fila2) >= 3 or abs(columna1 - columna2) >= 3

# Función para generar serpientes y escaleras aleatoriamente
def generar_serpientes_escaleras(num_serpientes, num_escaleras):
    celdas_validas = list(obtener_celdas_validas())
    random.shuffle(celdas_validas)
    
    serpientes = {}
    escaleras = {}
    
    # Crear serpientes
    while len(serpientes) < num_serpientes:
        inicio = random.choice(celdas_validas)
        fin = random.choice(celdas_validas)
        if inicio != fin and inicio > fin and not son_misma_fila_columna(inicio, fin) and es_diferencia_adecuada(inicio, fin):
            serpientes[inicio] = fin
            celdas_validas.remove(inicio)
            celdas_validas.remove(fin)
    
    # Crear escaleras
    while len(escaleras) < num_escaleras:
        inicio = random.choice(celdas_validas)
        fin = random.choice(celdas_validas)
        if inicio != fin and inicio < fin and not son_misma_fila_columna(inicio, fin) and es_diferencia_adecuada(inicio, fin):
            escaleras[inicio] = fin
            celdas_validas.remove(inicio)
            celdas_validas.remove(fin)
    
    return serpientes, escaleras

# Generar serpientes y escaleras
num_serpientes = 3  # Número de serpientes
num_escaleras = 3  # Número de escaleras
serpientes, escaleras = generar_serpientes_escaleras(num_serpientes, num_escaleras)

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
            casilla = (FILAS - 1 - fila) * COLUMNAS + (columna + 1) if fila % 2 == 0 else (FILAS - 1 - fila) * COLUMNAS + (COLUMNAS - columna)
            if casilla <= total_celdas:
                x = columna * TAMANIO_CASILLA
                y = fila * TAMANIO_CASILLA
                pygame.draw.rect(screen, BLANCO if casilla % 2 == 0 else NEGRO, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA))
                numero_texto = fuente.render(str(casilla), True, AZUL)
                screen.blit(numero_texto, (x + 5, y + 5))
            else:
                # Dibuja casillas vacías en el tablero
                x = columna * TAMANIO_CASILLA
                y = fila * TAMANIO_CASILLA
                pygame.draw.rect(screen, NEGRO, (x, y, TAMANIO_CASILLA, TAMANIO_CASILLA))

# Dibujar serpientes y escaleras
def dibujar_serpientes_escaleras():
    for inicio, fin in serpientes.items():
        if inicio <= total_celdas and fin <= total_celdas:
            x1, y1 = obtener_coordenadas(inicio)
            x2, y2 = obtener_coordenadas(fin)
            pygame.draw.line(screen, ROJO, (x1 + TAMANIO_CASILLA // 2, y1 + TAMANIO_CASILLA // 2), (x2 + TAMANIO_CASILLA // 2, y2 + TAMANIO_CASILLA // 2), 5)

    for inicio, fin in escaleras.items():
        if inicio <= total_celdas and fin <= total_celdas:
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
        if posicion_jugador < total_celdas:
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
