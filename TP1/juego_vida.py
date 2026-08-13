import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# -------------------------
# Configuración
# -------------------------

FILAS = 50
COLUMNAS = 50

PROBABILIDAD_VIVA = 0.25
INTERVALO_MS = 150


# -------------------------
# Crear tablero inicial
# -------------------------

def crear_tablero(filas, columnas):
    """
    Crea un tablero aleatorio.

    0 = célula muerta
    1 = célula viva
    """

    tablero = np.random.choice(
        [0, 1],
        size=(filas, columnas),
        p=[1 - PROBABILIDAD_VIVA, PROBABILIDAD_VIVA]
    )

    return tablero


# -------------------------
# Contar vecinos
# -------------------------

def contar_vecinos(tablero, fila, columna):
    """
    Cuenta cuántas células vivas rodean
    a una determinada célula.
    """

    filas, columnas = tablero.shape

    vecinos_vivos = 0

    for desplazamiento_fila in [-1, 0, 1]:
        for desplazamiento_columna in [-1, 0, 1]:

            # No contar la propia célula
            if desplazamiento_fila == 0 and desplazamiento_columna == 0:
                continue

            nueva_fila = fila + desplazamiento_fila
            nueva_columna = columna + desplazamiento_columna

            # Verificar que el vecino esté dentro del tablero
            if (
                0 <= nueva_fila < filas
                and 0 <= nueva_columna < columnas
            ):
                vecinos_vivos += tablero[nueva_fila, nueva_columna]

    return vecinos_vivos


# -------------------------
# Calcular nueva generación
# -------------------------

def siguiente_generacion(tablero):

    filas, columnas = tablero.shape

    # Creamos otro tablero para que los cambios sean simultáneos
    nuevo_tablero = np.zeros_like(tablero)

    for fila in range(filas):
        for columna in range(columnas):

            vecinos = contar_vecinos(
                tablero,
                fila,
                columna
            )

            celula_viva = tablero[fila, columna] == 1

            # Célula viva
            if celula_viva:

                # Vive si tiene 2 o 3 vecinos
                if vecinos == 2 or vecinos == 3:
                    nuevo_tablero[fila, columna] = 1

            # Célula muerta
            else:

                # Nace si tiene exactamente 3 vecinos
                if vecinos == 3:
                    nuevo_tablero[fila, columna] = 1

    return nuevo_tablero


# -------------------------
# Programa principal
# -------------------------

tablero = crear_tablero(FILAS, COLUMNAS)

figura, eje = plt.subplots()

imagen = eje.imshow(
    tablero,
    cmap="binary",
    interpolation="nearest"
)

eje.set_title("Juego de la Vida de Conway")

eje.set_xticks([])
eje.set_yticks([])


# -------------------------
# Animación
# -------------------------

def actualizar(frame):

    global tablero

    tablero = siguiente_generacion(tablero)

    imagen.set_data(tablero)

    eje.set_title(
        f"Juego de la Vida - Generación {frame}"
    )

    return [imagen]


animacion = FuncAnimation(
    figura,
    actualizar,
    interval=INTERVALO_MS,
    blit=False
)

plt.show()
