import pygame
import tkinter as tk
from tkinter import filedialog
import time
from typing import Tuple, List, Dict, Optional
from dfs import dfs, dfs_limited  # Importa l'algoritmo DFS

# Placeholder per gli altri algoritmi (creerai questi file separatamente)
# from a_star import a_star
# from bfs import bfs
# from ucs import ucs

# === CONFIGURAZIONE ===
CELL_SIZE = 10
SIDE_PANEL_WIDTH = 300
UNDER_PANEL_HEIGHT = 150

# === COLORI ===
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

# === CONFIGURAZIONE TERRENI ===
class TerrainType:
    def __init__(self, name: str, color: tuple, cost: int):
        self.name = name
        self.color = color + (120,)  # Aggiunge trasparenza
        self.cost = cost

# Dizionario dei tipi di terreno
terrain_types = {
    "verde": TerrainType("verde", (0, 255, 0), 3),
    "nero": TerrainType("nero", (0, 0, 0), 2),
    "bianco": TerrainType("bianco", (255, 255, 255), 1),
    "blu": TerrainType("blu", (0, 0, 255), 10)
}

# === CLASSE PRINCIPALE ===
class PathfindingGUI:
    def __init__(self, image_path: str):
        pygame.init()
        
        # Carica immagine
        self.image = pygame.image.load(image_path)
        self.img_width, self.img_height = self.image.get_size()
        
        # Finestra
        self.win_width = self.img_width + SIDE_PANEL_WIDTH
        self.win_height = self.img_height + UNDER_PANEL_HEIGHT
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("Pathfinding AI - Visualizzatore")
        
        # Font
        self.font_small = pygame.font.Font(None, 20)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 32)
        
        # Griglia
        self.num_cols = self.img_width // CELL_SIZE
        self.num_rows = self.img_height // CELL_SIZE
        self.cell_width = self.img_width // self.num_cols
        self.cell_height = self.img_height // self.num_rows
        
        # Superficie trasparente per la griglia
        self.grid_surface = pygame.Surface((self.img_width, self.img_height), pygame.SRCALPHA)
        
        # Griglia dati (0 = vuoto, stringa = tipo terreno)
        # Inizializziamo la griglia senza percorsi (vuota)
        self.grid = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        
        # Stato
        self.current_terrain = "verde"
        self.selected_algorithm = "A*"
        self.start_pos = None
        self.goal_pos = None
        self.path = []
        self.explored_nodes = []
        
        # Risultati
        self.last_cost = 0
        self.last_time = 0
        self.last_nodes_expanded = 0
        self.last_path_length = 0
        
        # Inizializziamo le liste che conterranno gli elementi della GUI
        self.buttons = []
        self.terrain_buttons = []
        self.algorithm_buttons = []
        self.cost_inputs = {}
        
        self._create_ui_elements()
        
    def _create_ui_elements(self):
        """Crea tutti gli elementi UI"""
        panel_x = self.img_width + 15
        y_offset = 50
        
        # Pulsanti selezione terreno con layout corretto
        y_offset += 30
        terrain_items = list(terrain_types.items())
        for i, (terrain_key, terrain) in enumerate(terrain_items):
            # Pulsante terreno
            btn = Button(
                panel_x, y_offset + i * 40,
                120, 35,
                terrain.name.upper(),
                terrain.color[:3],
                lambda t=terrain_key: self._select_terrain(t)
            )
            self.terrain_buttons.append(btn)
            
            # Pulsanti per modificare il costo
            minus_btn = Button(
                panel_x + 140, y_offset + i * 40,
                30, 35,
                "-",
                LIGHT_GRAY,
                lambda t=terrain_key: self._change_cost(t, -1)
            )
            
            # Il valore del costo sarà mostrato tra i due pulsanti (nel draw)
            
            plus_btn = Button(
                panel_x + 220, y_offset + i * 40,
                30, 35,
                "+",
                LIGHT_GRAY,
                lambda t=terrain_key: self._change_cost(t, 1)
            )
            self.buttons.extend([btn, minus_btn, plus_btn])
        
        # Pulsanti algoritmi
        y_offset += 180
        algorithms = ["A*", "BFS", "DFS", "UCS"]
        for i, algo in enumerate(algorithms):
            btn = Button(
                panel_x + (i % 2) * 135,
                y_offset + (i // 2) * 40,
                125, 35,
                algo,
                CYAN,
                lambda a=algo: self._select_algorithm(a)
            )
            self.algorithm_buttons.append(btn)
            self.buttons.append(btn)
        
        # Pulsanti controllo
        y_offset += 90
        self.buttons.append(Button(
            panel_x, y_offset,
            125, 35,
            "SET START",
            GREEN,
            self._set_start_mode
        ))
        self.buttons.append(Button(
            panel_x + 135, y_offset,
            125, 35,
            "SET GOAL",
            RED,
            self._set_goal_mode
        ))
        
        y_offset += 45
        self.buttons.append(Button(
            panel_x, y_offset,
            125, 35,
            "RUN",
            ORANGE,
            self._run_pathfinding
        ))
        self.buttons.append(Button(
            panel_x + 135, y_offset,
            125, 35,
            "CLEAR",
            GRAY,
            self._clear_path
        ))
        
        y_offset += 45
        self.buttons.append(Button(
            panel_x, y_offset,
            260, 35,
            "CLEAR ALL",
            DARK_GRAY,
            self._clear_all
        ))
        
    def _select_terrain(self, terrain_key: str):
        """Seleziona il terreno corrente"""
        self.current_terrain = terrain_key
        self.setting_start = False
        self.setting_goal = False
        
    def _select_algorithm(self, algo: str):
        """Seleziona l'algoritmo"""
        self.selected_algorithm = algo
        
    def _change_cost(self, terrain_key: str, delta: int):
        """Modifica il costo di un terreno"""
        terrain_types[terrain_key].cost = max(1, terrain_types[terrain_key].cost + delta)
        
    def _set_start_mode(self):
        """Modalità impostazione punto di partenza"""
        self.setting_start = True
        self.setting_goal = False
        
    def _set_goal_mode(self):
        """Modalità impostazione punto di arrivo"""
        self.setting_goal = True
        self.setting_start = False
        
    def _clear_path(self):
        """Cancella solo il percorso"""
        self.path = []
        self.explored_nodes = []
        
    def _clear_all(self):
        """Cancella tutto"""
        self.grid = [[0 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        self.start_pos = None
        self.goal_pos = None
        self.path = []
        self.explored_nodes = []
        self.last_cost = 0
        self.last_time = 0
        self.last_nodes_expanded = 0
        self.last_path_length = 0
        
    def _run_pathfinding(self):
        """Esegue l'algoritmo di pathfinding selezionato"""
        if not self.start_pos or not self.goal_pos:
            print("Imposta prima START e GOAL!")
            return
            
        # Prepara i costi per la griglia
        costs = self._prepare_cost_grid()
        
        # Misura il tempo di esecuzione
        start_time = time.time()
        
        # Esegue l'algoritmo selezionato
        if self.selected_algorithm == "DFS":
            # Usa DFS standard
            self.path, self.explored_nodes = dfs(self.start_pos, self.goal_pos, self.grid, costs)
            
            # Oppure usa DFS con limite di profondità per griglie grandi:
            # self.path, self.explored_nodes = dfs_limited(self.start_pos, self.goal_pos, self.grid, costs, max_depth=50)
            
        elif self.selected_algorithm == "A*":
            # Quando avrai implementato A*
            # self.path, self.explored_nodes = a_star(self.start_pos, self.goal_pos, self.grid, costs)
            print("A* non ancora implementato")
            self.path = []
            self.explored_nodes = []
            
        elif self.selected_algorithm == "BFS":
            # Quando avrai implementato BFS
            # self.path, self.explored_nodes = bfs(self.start_pos, self.goal_pos, self.grid, costs)
            print("BFS non ancora implementato")
            self.path = []
            self.explored_nodes = []
            
        elif self.selected_algorithm == "UCS":
            # Quando avrai implementato UCS
            # self.path, self.explored_nodes = ucs(self.start_pos, self.goal_pos, self.grid, costs)
            print("UCS non ancora implementato")
            self.path = []
            self.explored_nodes = []
        
        end_time = time.time()
        
        # Aggiorna statistiche
        self.last_time = (end_time - start_time) * 1000  # in millisecondi
        self.last_nodes_expanded = len(self.explored_nodes)
        self.last_path_length = len(self.path)
        self.last_cost = self._calculate_path_cost()
        
        # Stampa risultati per debug
        if self.path:
            print(f"Percorso trovato con {self.selected_algorithm}!")
            print(f"Lunghezza: {self.last_path_length}, Costo: {self.last_cost}")
        else:
            print(f"Nessun percorso trovato con {self.selected_algorithm}")
        
    def _prepare_cost_grid(self) -> List[List[int]]:
        """Prepara una griglia con i costi"""
        costs = [[1 for _ in range(self.num_cols)] for _ in range(self.num_rows)]
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                terrain = self.grid[row][col]
                if terrain and terrain in terrain_types:
                    costs[row][col] = terrain_types[terrain].cost
        return costs
        
    def _calculate_path_cost(self) -> int:
        """Calcola il costo totale del percorso"""
        if not self.path:
            return 0
        total_cost = 0
        for row, col in self.path:
            terrain = self.grid[row][col]
            if terrain and terrain in terrain_types:
                total_cost += terrain_types[terrain].cost
            else:
                total_cost += 1
        return total_cost
        
    def _handle_mouse_click(self, pos: Tuple[int, int], button: int):
        """Gestisce i click del mouse"""
        x, y = pos
        
        # Click sulla griglia
        if x < self.img_width and y < self.img_height:
            col = x // self.cell_width
            row = y // self.cell_height
            
            if 0 <= row < self.num_rows and 0 <= col < self.num_cols:
                if hasattr(self, 'setting_start') and self.setting_start:
                    self.start_pos = (row, col)
                    self.setting_start = False
                elif hasattr(self, 'setting_goal') and self.setting_goal:
                    self.goal_pos = (row, col)
                    self.setting_goal = False
                elif button == 1:  # Click sinistro
                    self.grid[row][col] = self.current_terrain
                elif button == 3:  # Click destro
                    self.grid[row][col] = 0
                    
    def _draw_grid(self):
        """Disegna la griglia con i terreni"""
        self.grid_surface.fill((0, 0, 0, 0))
        
        # Disegna i terreni
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                terrain = self.grid[row][col]
                if terrain and terrain in terrain_types:
                    color = terrain_types[terrain].color
                    rect = pygame.Rect(
                        col * self.cell_width,
                        row * self.cell_height,
                        self.cell_width,
                        self.cell_height
                    )
                    pygame.draw.rect(self.grid_surface, color, rect)
                    
        # Disegna nodi esplorati
        for row, col in self.explored_nodes:
            rect = pygame.Rect(
                col * self.cell_width,
                row * self.cell_height,
                self.cell_width,
                self.cell_height
            )
            pygame.draw.rect(self.grid_surface, (255, 255, 0, 60), rect)
            
        # Disegna il percorso
        for row, col in self.path:
            rect = pygame.Rect(
                col * self.cell_width,
                row * self.cell_height,
                self.cell_width,
                self.cell_height
            )
            pygame.draw.rect(self.grid_surface, (255, 0, 255, 120), rect)
            
        # Disegna start e goal
        if self.start_pos:
            row, col = self.start_pos
            rect = pygame.Rect(
                col * self.cell_width,
                row * self.cell_height,
                self.cell_width,
                self.cell_height
            )
            pygame.draw.rect(self.grid_surface, GREEN, rect)
            
        if self.goal_pos:
            row, col = self.goal_pos
            rect = pygame.Rect(
                col * self.cell_width,
                row * self.cell_height,
                self.cell_width,
                self.cell_height
            )
            pygame.draw.rect(self.grid_surface, RED, rect)
            
    def _draw_side_panel(self):
        """Disegna il pannello laterale"""
        # Sfondo pannello
        pygame.draw.rect(self.win, DARK_GRAY, (self.img_width, 0, SIDE_PANEL_WIDTH, self.img_height))
        
        # Titolo
        title = self.font_large.render("CONTROLLI", True, WHITE)
        title_rect = title.get_rect(centerx=self.img_width + SIDE_PANEL_WIDTH // 2, y=10)
        self.win.blit(title, title_rect)
        
        # Sezione terreni
        y_offset = 55
        terrain_title = self.font_medium.render("Terreni (costo):", True, WHITE)
        self.win.blit(terrain_title, (self.img_width + 15, y_offset))
        
        # Mostra costi terreni e indicatore selezione
        y_offset += 35
        for i, (terrain_key, terrain) in enumerate(terrain_types.items()):
            # Indicatore terreno selezionato
            if self.current_terrain == terrain_key:
                pygame.draw.rect(self.win, WHITE, (self.img_width + 10, y_offset + i * 40 - 3, 270, 41), 2)
                
            # Mostra costo centrato tra i pulsanti +/-
            cost_text = self.font_large.render(f"{terrain.cost}", True, WHITE)
            cost_rect = cost_text.get_rect(center=(self.img_width + 195, y_offset + i * 40 + 17))
            self.win.blit(cost_text, cost_rect)
            
        # Sezione algoritmi
        y_offset += 190
        algo_title = self.font_medium.render("Algoritmo:", True, WHITE)
        self.win.blit(algo_title, (self.img_width + 15, y_offset))
        
        # Indicatore algoritmo selezionato
        for btn in self.algorithm_buttons:
            if btn.text == self.selected_algorithm:
                pygame.draw.rect(self.win, WHITE, (btn.x - 3, btn.y - 3, btn.width + 6, btn.height + 6), 2)
                
        # Sezione controlli
        y_offset += 90
        controls_title = self.font_medium.render("Controlli:", True, WHITE)
        self.win.blit(controls_title, (self.img_width + 15, y_offset))
        
        # Indicatori start/goal se impostati
        if self.start_pos:
            start_text = self.font_small.render(f"Start: {self.start_pos}", True, GREEN)
            self.win.blit(start_text, (self.img_width + 15, self.img_height - 60))
            
        if self.goal_pos:
            goal_text = self.font_small.render(f"Goal: {self.goal_pos}", True, RED)
            self.win.blit(goal_text, (self.img_width + 15, self.img_height - 40))
                
    def _draw_bottom_panel(self):
        """Disegna il pannello inferiore con i risultati"""
        # Sfondo
        pygame.draw.rect(self.win, BLACK, (0, self.img_height, self.win_width, UNDER_PANEL_HEIGHT))
        pygame.draw.line(self.win, WHITE, (0, self.img_height), (self.win_width, self.img_height), 2)
        
        # Titolo
        title = self.font_large.render("RISULTATI", True, WHITE)
        self.win.blit(title, (10, self.img_height + 10))
        
        # Risultati in colonne
        y_base = self.img_height + 50
        col_width = self.win_width // 4
        
        results = [
            ("Costo totale:", f"{self.last_cost}"),
            ("Tempo (ms):", f"{self.last_time:.2f}"),
            ("Nodi espansi:", f"{self.last_nodes_expanded}"),
            ("Lungh. percorso:", f"{self.last_path_length}")
        ]
        
        for i, (label, value) in enumerate(results):
            x = 10 + (i % 2) * col_width * 2
            y = y_base + (i // 2) * 40
            
            label_text = self.font_medium.render(label, True, LIGHT_GRAY)
            value_text = self.font_large.render(value, True, WHITE)
            
            self.win.blit(label_text, (x, y))
            self.win.blit(value_text, (x + 150, y))
            
    def run(self):
        """Loop principale"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse_click(pygame.mouse.get_pos(), event.button)
                elif event.type == pygame.KEYDOWN:
                    # Scorciatoie tastiera
                    if event.key == pygame.K_1:
                        self.current_terrain = "verde"
                    elif event.key == pygame.K_2:
                        self.current_terrain = "nero"
                    elif event.key == pygame.K_3:
                        self.current_terrain = "bianco"
                    elif event.key == pygame.K_4:
                        self.current_terrain = "blu"
                    elif event.key == pygame.K_s:
                        self._set_start_mode()
                    elif event.key == pygame.K_g:
                        self._set_goal_mode()
                    elif event.key == pygame.K_SPACE:
                        self._run_pathfinding()
                        
            # Gestione click continuo
            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0] or mouse_pressed[2]:
                self._handle_mouse_click(pygame.mouse.get_pos(), 1 if mouse_pressed[0] else 3)
                
            # Update pulsanti
            for button in self.buttons:
                button.update()
                
            # Disegna tutto
            self.win.blit(self.image, (0, 0))
            self._draw_grid()
            self.win.blit(self.grid_surface, (0, 0))
            self._draw_side_panel()
            self._draw_bottom_panel()
            
            # Disegna pulsanti
            for button in self.buttons:
                button.draw(self.win)
                
            pygame.display.flip()
            clock.tick(60)
            
        pygame.quit()


# === CLASSE BUTTON ===
class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = tuple(min(255, c + 50) for c in color[:3])
        self.action = action
        self.hovered = False
        self.font = pygame.font.Font(None, 22)
        self.clicked = False
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        self.hovered = (self.x < mouse_pos[0] < self.x + self.width and
                       self.y < mouse_pos[1] < self.y + self.height)
        
        # Gestione click con debounce
        if self.hovered and mouse_click and not self.clicked:
            self.action()
            self.clicked = True
        elif not mouse_click:
            self.clicked = False
            
    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2)
        
        text_surface = self.font.render(self.text, True, BLACK if sum(color[:3]) > 400 else WHITE)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surface, text_rect)


# === MAIN ===
if __name__ == "__main__":
    # Selettore file
    tk.Tk().withdraw()
    file_path = filedialog.askopenfilename(
        title="Seleziona la mappa (immagine)",
        filetypes=[("Immagini", "*.png *.jpg *.jpeg *.bmp")]
    )
    
    if file_path:
        gui = PathfindingGUI(file_path)
        gui.run()
    else:
        print("Nessun file selezionato.")