"""
Depth-First Search (DFS) Algorithm for Pathfinding
Supporta movimento in 8 direzioni
"""

from typing import Tuple, List, Set, Dict, Optional


def dfs(start_pos: Tuple[int, int], 
        goal_pos: Tuple[int, int], 
        grid: List[List[any]], 
        costs: List[List[int]]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Implementa l'algoritmo DFS per il pathfinding.
    
    Args:
        start_pos: Tupla (row, col) della posizione di partenza
        goal_pos: Tupla (row, col) della posizione obiettivo
        grid: Matrice con i tipi di terreno (0 = vuoto, stringa = tipo terreno)
        costs: Matrice con i costi numerici per ogni cella
        
    Returns:
        path: Lista di tuple (row, col) che rappresenta il percorso trovato
        explored_nodes: Lista di tuple (row, col) dei nodi esplorati durante la ricerca
    """
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Direzioni di movimento (8 direzioni: N, NE, E, SE, S, SW, W, NW)
    directions = [
        (-1, 0),   # Nord
        (-1, 1),   # Nord-Est
        (0, 1),    # Est
        (1, 1),    # Sud-Est
        (1, 0),    # Sud
        (1, -1),   # Sud-Ovest
        (0, -1),   # Ovest
        (-1, -1)   # Nord-Ovest
    ]
    
    # Stack per DFS: contiene (posizione, percorso)
    stack = [(start_pos, [start_pos])]
    
    # Set per tenere traccia dei nodi visitati
    visited = set()
    visited.add(start_pos)
    
    # Lista dei nodi esplorati (per visualizzazione)
    explored_nodes = []
    
    while stack:
        current_pos, path = stack.pop()
        row, col = current_pos
        
        # Aggiungi ai nodi esplorati
        explored_nodes.append(current_pos)
        
        # Controlla se abbiamo raggiunto l'obiettivo
        if current_pos == goal_pos:
            return path, explored_nodes
        
        # Esplora i vicini in ordine inverso (per DFS standard da sinistra a destra)
        for i in range(len(directions) - 1, -1, -1):
            dy, dx = directions[i]
            new_row, new_col = row + dy, col + dx
            new_pos = (new_row, new_col)
            
            # Verifica se la nuova posizione è valida
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                new_pos not in visited):
                
                # Verifica che non sia un ostacolo (assumiamo che costo 999 = ostacolo)
                if costs[new_row][new_col] < 999:
                    visited.add(new_pos)
                    new_path = path + [new_pos]
                    stack.append((new_pos, new_path))
    
    # Se non trova un percorso, ritorna liste vuote
    return [], explored_nodes


def dfs_limited(start_pos: Tuple[int, int], 
                goal_pos: Tuple[int, int], 
                grid: List[List[any]], 
                costs: List[List[int]],
                max_depth: int = 100) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Versione di DFS con limite di profondità per evitare ricerche infinite.
    
    Args:
        start_pos: Posizione di partenza
        goal_pos: Posizione obiettivo
        grid: Griglia con i terreni
        costs: Griglia con i costi
        max_depth: Profondità massima di ricerca
        
    Returns:
        path: Percorso trovato
        explored_nodes: Nodi esplorati
    """
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    directions = [
        (-1, 0), (-1, 1), (0, 1), (1, 1),
        (1, 0), (1, -1), (0, -1), (-1, -1)
    ]
    
    # Stack: (posizione, percorso, profondità)
    stack = [(start_pos, [start_pos], 0)]
    visited = set()
    visited.add(start_pos)
    explored_nodes = []
    
    while stack:
        current_pos, path, depth = stack.pop()
        explored_nodes.append(current_pos)
        
        if current_pos == goal_pos:
            return path, explored_nodes
            
        # Non espandere oltre il limite di profondità
        if depth >= max_depth:
            continue
            
        row, col = current_pos
        
        for i in range(len(directions) - 1, -1, -1):
            dy, dx = directions[i]
            new_row, new_col = row + dy, col + dx
            new_pos = (new_row, new_col)
            
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                new_pos not in visited and
                costs[new_row][new_col] < 999):
                
                visited.add(new_pos)
                new_path = path + [new_pos]
                stack.append((new_pos, new_path, depth + 1))
    
    return [], explored_nodes


def dfs_recursive(start_pos: Tuple[int, int], 
                  goal_pos: Tuple[int, int], 
                  grid: List[List[any]], 
                  costs: List[List[int]]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Implementazione ricorsiva di DFS (per riferimento).
    Nota: Potrebbe causare stack overflow su griglie molto grandi.
    """
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    visited = set()
    explored_nodes = []
    path_found = []
    
    directions = [
        (-1, 0), (-1, 1), (0, 1), (1, 1),
        (1, 0), (1, -1), (0, -1), (-1, -1)
    ]
    
    def dfs_visit(pos: Tuple[int, int], path: List[Tuple[int, int]]) -> bool:
        nonlocal path_found
        
        if pos in visited:
            return False
            
        visited.add(pos)
        explored_nodes.append(pos)
        
        if pos == goal_pos:
            path_found = path
            return True
            
        row, col = pos
        
        for dy, dx in directions:
            new_row, new_col = row + dy, col + dx
            new_pos = (new_row, new_col)
            
            if (0 <= new_row < rows and 
                0 <= new_col < cols and 
                new_pos not in visited and
                costs[new_row][new_col] < 999):
                
                if dfs_visit(new_pos, path + [new_pos]):
                    return True
                    
        return False
    
    dfs_visit(start_pos, [start_pos])
    return path_found, explored_nodes


# Funzione helper per testare l'algoritmo
def create_test_grid(rows: int, cols: int, obstacles: List[Tuple[int, int]] = None) -> Tuple[List[List[int]], List[List[int]]]:
    """
    Crea una griglia di test con ostacoli opzionali.
    """
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    costs = [[1 for _ in range(cols)] for _ in range(rows)]
    
    if obstacles:
        for row, col in obstacles:
            if 0 <= row < rows and 0 <= col < cols:
                grid[row][col] = "obstacle"
                costs[row][col] = 999
                
    return grid, costs


# Test dell'algoritmo
if __name__ == "__main__":
    # Crea una griglia di test 10x10 con alcuni ostacoli
    obstacles = [(2, 2), (2, 3), (2, 4), (3, 2), (4, 2)]
    grid, costs = create_test_grid(10, 10, obstacles)
    
    start = (0, 0)
    goal = (5, 5)
    
    print("Test DFS standard:")
    path, explored = dfs(start, goal, grid, costs)
    print(f"Percorso trovato: {path}")
    print(f"Nodi esplorati: {len(explored)}")
    
    print("\nTest DFS con limite di profondità:")
    path, explored = dfs_limited(start, goal, grid, costs, max_depth=20)
    print(f"Percorso trovato: {path}")
    print(f"Nodi esplorati: {len(explored)}")