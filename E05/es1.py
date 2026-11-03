import somme
#import numpy as np
#somme.somma_naturali__doc__
#somme.somma_sqrt__doc__
help(somme.somma_naturali)
help(somme.somma_sqrt)  
print("somma con n=150:", somme.somma_naturali(150))
print("somma delle radici quadrate con n=150:", somme.somma_sqrt(150))

print("================================================================================")
help(somme.somma_prod)
print("somma con n=15:", somme.somma_prod(15)[0])
print("prodotto con n=15:", somme.somma_prod(15)[1])
print("================================================================================")
help(somme.somma_alfa)
print("somma con n=15 e alfa=2:", somme.somma_alfa(15, 2))
print("somma con n=15 e alfa=0.5:", somme.somma_alfa(15, 0.5))