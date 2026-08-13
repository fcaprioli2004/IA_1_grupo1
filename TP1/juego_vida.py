import pygame
import random


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Tamaño de la ventana en píxeles.
WIDTH = 1000
HEIGHT = 800

# Tamaño de cada célula en píxeles.
CELL_SIZE = 10

# Cantidad de filas y columnas del tablero.
COLUMNAS = WIDTH // CELL_SIZE
FILAS = HEIGHT // CELL_SIZE

# Velocidad de la simulación.
FPS = 10

# Probabilidad inicial de que una célula esté viva.
PROBABILIDAD_VIVA = 0.25


# ============================================================
# COLORES
# ============================================================

COLOR_FONDO = (240, 240, 240)
COLOR_CELULA_VIVA = (30, 30, 30)
COLOR_GRILLA = (210, 210, 210)


# ============================================================
# CREACIÓN DEL TABLERO
# ============================================================

def crear_tablero():
    """
    Crea un tablero con células vivas y muertas de forma aleatoria.

    0 = célula muerta
    1 = célula viva
    """

    tablero = []

    for fila in range(FILAS):

        nueva_fila = []

        for columna in range(COLUMNAS):

            if random.random() < PROBABILIDAD_VIVA:
                nueva_fila.append(1)
            else:
                nueva_fila.append(0)

        tablero.append(nueva_fila)

    return tablero


# ============================================================
# CONTEO DE VECINOS
# ============================================================

def contar_vecinos(tablero, fila, columna):
    """
    Cuenta cuántas células vivas rodean a una célula.

    Se analizan las ocho posiciones vecinas.
    Las posiciones fuera del tablero se consideran muertas.
    """

    vecinos_vivos = 0

    # Recorremos las ocho posiciones que rodean a la célula.
    for desplazamiento_fila in (-1, 0, 1):
        for desplazamiento_columna in (-1, 0, 1):

            # No contamos la propia célula.
            if desplazamiento_fila == 0 and desplazamiento_columna == 0:
                continue

            fila_vecina = fila + desplazamiento_fila
            columna_vecina = columna + desplazamiento_columna

            # Verificamos que la posición esté dentro del tablero.
            if (
                0 <= fila_vecina < FILAS
                and 0 <= columna_vecina < COLUMNAS
            ):
                vecinos_vivos += tablero[fila_vecina][columna_vecina]

    return vecinos_vivos


# ============================================================
# SIGUIENTE GENERACIÓN
# ============================================================

def siguiente_generacion(tablero):
    """
    Calcula el estado completo de la siguiente generación.

    Se utiliza un tablero nuevo para que todas las células
    cambien de estado de manera simultánea.
    """

    # Inicialmente todas las células de la nueva generación están muertas.
    nuevo_tablero = [
        [0 for columna in range(COLUMNAS)]
        for fila in range(FILAS)
    ]

    for fila in range(FILAS):
        for columna in range(COLUMNAS):

            vecinos_vivos = contar_vecinos(tablero, fila, columna)
            celula_viva = tablero[fila][columna] == 1

            # Una célula viva sobrevive si tiene 2 o 3 vecinos vivos.
            if celula_viva and vecinos_vivos in (2, 3):
                nuevo_tablero[fila][columna] = 1

            # Una célula muerta nace si tiene exactamente 3 vecinos vivos.
            elif not celula_viva and vecinos_vivos == 3:
                nuevo_tablero[fila][columna] = 1

            # En cualquier otro caso la célula queda muerta.

    return nuevo_tablero


# ============================================================
# DIBUJO DEL TABLERO
# ============================================================

def dibujar_tablero(pantalla, tablero):
    """
    Dibuja las células vivas y la grilla sobre la pantalla.
    """

    pantalla.fill(COLOR_FONDO)

    # Dibujar las células vivas.
    for fila in range(FILAS):
        for columna in range(COLUMNAS):

            if tablero[fila][columna] == 1:

                x = columna * CELL_SIZE
                y = fila * CELL_SIZE

                celda = pygame.Rect(
                    x,
                    y,
                    CELL_SIZE,
                    CELL_SIZE
                )

                pygame.draw.rect(
                    pantalla,
                    COLOR_CELULA_VIVA,
                    celda
                )

    # Dibujar líneas verticales.
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(
            pantalla,
            COLOR_GRILLA,
            (x, 0),
            (x, HEIGHT)
        )

    # Dibujar líneas horizontales.
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(
            pantalla,
            COLOR_GRILLA,
            (0, y),
            (WIDTH, y)
        )


# ============================================================
# INICIO DE PYGAME
# ============================================================

pygame.init()

pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de la Vida de Conway")

reloj = pygame.time.Clock()


# ============================================================
# ESTADO INICIAL
# ============================================================

tablero = crear_tablero()

ejecutando = True
pausado = False
generacion = 0


# ============================================================
# BUCLE PRINCIPAL
# ============================================================

while ejecutando:

    # --------------------------------------------------------
    # Eventos
    # --------------------------------------------------------

    for evento in pygame.event.get():

        # Cerrar la ventana.
        if evento.type == pygame.QUIT:
            ejecutando = False

        # Controles mediante teclado.
        elif evento.type == pygame.KEYDOWN:

            # ESPACIO: pausar o continuar.
            if evento.key == pygame.K_SPACE:
                pausado = not pausado

            # R: crear un tablero aleatorio nuevo.
            elif evento.key == pygame.K_r:
                tablero = crear_tablero()
                generacion = 0

            # C: limpiar completamente el tablero.
            elif evento.key == pygame.K_c:

                tablero = [
                    [0 for columna in range(COLUMNAS)]
                    for fila in range(FILAS)
                ]

                generacion = 0

            # N: avanzar una generación manualmente si está pausado.
            elif evento.key == pygame.K_n and pausado:

                tablero = siguiente_generacion(tablero)
                generacion += 1

        # ----------------------------------------------------
        # Modificar células con el mouse
        # ----------------------------------------------------

        elif evento.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            columna = mouse_x // CELL_SIZE
            fila = mouse_y // CELL_SIZE

            # Cambiar el estado de la célula seleccionada.
            tablero[fila][columna] = 1 - tablero[fila][columna]


    # --------------------------------------------------------
    # Actualizar simulación
    # --------------------------------------------------------

    if not pausado:

        tablero = siguiente_generacion(tablero)
        generacion += 1


    # --------------------------------------------------------
    # Renderizado
    # --------------------------------------------------------

    dibujar_tablero(pantalla, tablero)


    # Actualizar el título de la ventana.
    if pausado:
        estado = "PAUSADO"
    else:
        estado = "EJECUTANDO"

    pygame.display.set_caption(
        f"Juego de la Vida - Generación: {generacion} | {estado}"
    )


    # Mostrar el nuevo frame.
    pygame.display.flip()


    # Limitar la velocidad de la simulación.
    reloj.tick(FPS)


# ============================================================
# CIERRE
# ============================================================

pygame.quit()