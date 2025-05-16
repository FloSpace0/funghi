from PIL import Image
import numpy as np

# Carica l'immagine
img = Image.open("mappa.png").convert("L")  # Converti in bianco e nero
img = img.resize((100, 100))  # Riduci la dimensione se è troppo grande

# Converti in matrice NumPy
data = np.array(img)

# Crea griglia: 0 = strada (chiaro), 1 = ostacolo (scuro)
griglia = (data < 128).astype(int)

# Visualizza la matrice
for riga in griglia:
    print("".join(str(c) for c in riga))
