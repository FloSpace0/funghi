import pygame
import tkinter as tk
from tkinter import filedialog

# === CONFIGURAZIONE ===
CELL_SIZE = 10  # dimensione in pixel di ogni cella
CELL_COLOR = (0, 0, 0, 120)  # Nero semi-trasparente

# === MAPPA COLORI ===
terrain_colors = {
    "nero": (0, 0, 0, 120),         # terra
    "bianco": (255, 255, 255, 120), # asfalto
    "verde": (0, 255, 0, 120),      # campo
    "blu": (0, 0, 255, 120)         # acqua
}

# === SELETTORE FILE ===
tk.Tk().withdraw()
file_path = filedialog.askopenfilename(
    title="Seleziona la mappa (immagine)",
    filetypes=[("Immagini", "*.png *.jpg *.jpeg *.bmp")]
)

if not file_path:
    print("Nessun file selezionato.")
    exit()

# === INIZIALIZZAZIONE ===
pygame.init()
image = pygame.image.load(file_path)
img_width, img_height = image.get_size()
win = pygame.display.set_mode((img_width, img_height))
pygame.display.set_caption("Trova Funghi 🍄")

# === CALCOLO GRIGLIA ADATTIVA ===
NUM_COLS = img_width // CELL_SIZE
NUM_ROWS = img_height // CELL_SIZE
cell_width = img_width // NUM_COLS
cell_height = img_height // NUM_ROWS

# === SUPERFICIE TRASPARENTE ===
grid_surface = pygame.Surface((img_width, img_height), pygame.SRCALPHA)

# === GRIGLIA (0 = vuoto, 1 = barriera) ===
grid = [[0 for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]

# === FUNZIONE PER DISEGNARE LA GRIGLIA ===
def draw_grid():
    grid_surface.fill((0, 0, 0, 0))  # Pulisce la superficie trasparente
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            terrain = grid[row][col]
            if terrain:
                color = terrain_colors[terrain]
                rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
                pygame.draw.rect(grid_surface, color, rect)


# === LOOP PRINCIPALE ===
running = True
current_terrain = "nero"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_KP0:
            current_terrain = "nero"
        elif event.key == pygame.K_KP1:
            current_terrain = "bianco"
        elif event.key == pygame.K_KP2:
            current_terrain = "verde"
        elif event.key == pygame.K_KP3:
            current_terrain = "blu"
        print(current_terrain)

            
    # Se tasto sinistro o destro è premuto
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0] or mouse_pressed[2]:  # sinistro o destro
        x, y = pygame.mouse.get_pos()
        col = x // CELL_SIZE
        row = y // CELL_SIZE

        if 0 <= row < NUM_ROWS and 0 <= col < NUM_COLS:
            if mouse_pressed[0]:  # sinistro
                grid[row][col] = current_terrain

            elif mouse_pressed[2]:  # destro
                grid[row][col] = 0

    # --- Disegna ---
    win.blit(image, (0, 0))  # sfondo
    draw_grid()
    win.blit(grid_surface, (0, 0))  # griglia trasparente sopra
    pygame.display.update()
