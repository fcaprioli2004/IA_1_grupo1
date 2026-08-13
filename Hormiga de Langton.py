import pygame
import sys

#Configuración de la ventana
WIDTH, HEIGHT = 1000, 800  # Tamaño de la ventana (pixeles)
CELL_SIZE = 5            # tamaño de cada celda (pixeles)
# Velocidad de simulación
STEPS_PER_FRAME = 8     

# Colores (R, G, B)
BG_COLOR = (240, 240, 240)  # Color del fondo
BLACK_CELL = (30, 30, 30)  # Color del camino
ANT_COLOR = (255, 69, 0)   # Color de la hormiga

# Vectores de dirección para la hormiga: Norte, Este, Sur, Oeste
# En pygame, el eje Y crece hacia abajo, por lo que Norte es (0, -1)
DIRECTIONS = [
    (0, -1),  # North
    (1, 0),   # East
    (0, 1),   # South
    (-1, 0)   # West
]

# --- Inicio de Pygame ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hormiga de Langton")
clock = pygame.time.Clock()

# --- Simulacion ---
# Al principio, es todo blanco, así que solo necesitamos almacenar las celdas negras.
black_cells = set()

# Se definen las condiciones iniciales de la hormiga (posición y dirección)
ant_x, ant_y = 0, 0
ant_direction = 3  

# Bucle de juego
running = True
steps = 0
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                if paused:
                    pygame.display.set_caption("Langton's Ant - PAUSED")
                else:
                    pygame.display.set_caption(f"Langton's Ant - Steps: {steps}")

    if paused:
        continue

    # Este for admite la posibilidad de ejecutar múltiples pasos de la simulación por cada frame renderizado, lo que permite una simulación más rápida.
    for _ in range(STEPS_PER_FRAME):
        current_pos = (ant_x, ant_y)
        
        # Lógica de la hormiga: según el color de la celda actual, gira y cambia el color de la celda.
        if current_pos in black_cells:
            # Si la celda es negra: Gira 90 a la izquierda, cambia el color de la celda a blanca
            ant_direction = (ant_direction - 1) % 4
            black_cells.remove(current_pos)
        else:
            # Si la celda es blanca: Gira 90 a la derecha, cambia el color de la celda a negra
            ant_direction = (ant_direction + 1) % 4
            black_cells.add(current_pos)

        # Mover la hormiga a la siguiente celda según su dirección actual
        dx, dy = DIRECTIONS[ant_direction]
        ant_x += dx
        ant_y += dy
        steps += 1

    # 4.Renderizado
    screen.fill(BG_COLOR)  # Resetea la pantalla a blanco antes de dibujar las celdas negras y la hormiga.

    # Se centra el (0,0)
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    # Se dibujan todas las celdas negras almacenadas en black_cells
    for bx, by in black_cells:
        # Convierte las coordenadas de la celda a coordenadas de pantalla
        rect_x = center_x + (bx * CELL_SIZE)
        rect_y = center_y + (by * CELL_SIZE)
        
        # Dibuja el rectángulo negro correspondiente a la celda
        cell_rect = pygame.Rect(rect_x, rect_y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, BLACK_CELL, cell_rect)

    # Dibuja la posición actual de la hormiga (marcador opcional, útil para ver su ubicación)
    ant_rect_x = center_x + (ant_x * CELL_SIZE)
    ant_rect_y = center_y + (ant_y * CELL_SIZE)
    ant_rect = pygame.Rect(ant_rect_x, ant_rect_y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, ANT_COLOR, ant_rect)

    # 5. Display Flip and Framerate control
    pygame.display.flip()
    
    # Se establecen los fotogramas por segundo
    clock.tick(60) 
    
    # Update title bar info every frame (without flickering title too fast)
    if steps % (STEPS_PER_FRAME * 2) == 0:
        pygame.display.set_caption(f"Hormiga de Langton - Pasos: {steps} | Celdas: {len(black_cells)}")

# Se cierra el juego
pygame.quit()
sys.exit()