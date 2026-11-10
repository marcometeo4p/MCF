import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return 0.003 *x**2
N=100000
def distr(N):
    x=np.random.uniform(0, 10, N)
    y=np.random.uniform(0, f(10), N)
    mask=y <= f(x)
    accepted_x = x[mask]
    print(f"Numero di campioni accettati: {len(accepted_x)} su {N}")
    return accepted_x

pr=distr(N)
plt.figure(figsize=(12, 9))
plt.hist(pr, bins=30, density=True, alpha=0.6, color='lightcoral', edgecolor='black', label='Campioni accettati')
# Sovrapponi la funzione di densità di probabilità teorica
x_theory = np.linspace(0, 10, 500)
y_theory = f(x_theory)
plt.plot(x_theory, y_theory, color="olive", linestyle='-', lw=2.5, label='PDF teorica')
plt.xlabel('x')
plt.title('Metodo Hit-or-Miss')
plt.ylabel('Densità di probabilità')
plt.legend(title=f"numero di campioni utilizzati: {len(pr)}")
plt.grid(True, alpha=0.3)
plt.savefig('hit_or_miss.png')
plt.show()


def cumulativa(n):
    # F(x) = x^3 / 1000  ==>  x = 10 * u^(1/3) per u ~ U(0, 1)
    u = np.random.uniform(0, 1, n)
    return 10.0 * (u ** (1 / 3))

x_c=cumulativa(N)
plt.figure(figsize=(12, 9))
plt.hist(x_c, bins=30, density=True, alpha=0.6, color='lightcoral', edgecolor='black', label='Campioni generati')
# Sovrapponi la funzione di densità di probabilità teorica
x_theory = np.linspace(0, 10, 500)
y_theory = f(x_theory)
plt.plot(x_theory, y_theory, color="steelblue", linestyle='-', lw=2.5, label='PDF teorica')
plt.xlabel('x')
plt.title('Distribuzione cumulativa')
plt.ylabel('Densità di probabilità')
plt.legend(title=f"numero di campioni utilizzati: {len(x_c)}")
plt.grid(True, alpha=0.3)
plt.savefig('cumulativa.png')
plt.show()