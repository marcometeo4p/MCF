import numpy as np

import numpy as np

def spost(N, s):
    """
    Genera una traiettoria (random walk) bidimensionale con N passi casuali.
    Parte da (0,0) ed esegue passi di lunghezza costante 's' in direzioni casuali.
    """
    # Genera N angoli casuali tra 0 e 2pi
    phi = np.random.uniform(0, 2*np.pi, N)
    
    # Calcola le componenti x e y di ciascun singolo passo
    dx = s * np.cos(phi)
    dy = s * np.sin(phi)
    
    # Inserisce il punto di partenza (0,0) all'inizio degli spostamenti
    x = np.concatenate(([0.0], np.cumsum(dx)))
    y = np.concatenate(([0.0], np.cumsum(dy)))
    
    # Restituisce una matrice 2x(N+1) dove la prima riga è X e la seconda è Y
    return np.array([x, y])

