import pygame
import tkinter as tk
from tkinter import filedialog

pygame.init()

# Dimensione della finestra
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Interfaccia Pygame")

# Font
font = pygame.font.SysFont(None, 48)

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Funzione per disegnare un pulsante
def draw_button(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Controllo hover
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))

    # Scritta sul pulsante
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_surface, text_rect)

# Azione da eseguire quando si clicca il pulsante
def start_game():
    print("Hai cliccato il pulsante Start!")

# Loop principale
running = True
while running:
    screen.fill(WHITE)

    # Disegna il pulsante ogni frame
    draw_button("Start", 200, 150, 200, 60, (0, 200, 0), (0, 255, 0), start_game)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
