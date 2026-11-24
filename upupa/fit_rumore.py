import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

# 1. Modello fisico: velocità radiale v_r(t) = A * cos(w * t + phi)
def v_radiale_fit(t, A, w, phi):
    return A * np.cos(w * t + phi)

# Parametri "veri" del sistema stella-pianeta (es. un Giove caldo)
A_vero = 55.0               # Semi-ampiezza [m/s]
P_vero = 4.2                # Periodo orbitale [giorni]
w_vero = 2 * np.pi / P_vero # Pulsazione [rad/giorno]
phi_vero = 0.8              # Fase iniziale [rad]

# 2. Simulazione dei dati sperimentali
np.random.seed(42)  # Per rendere ripetibile la simulazione

N_misure = 45       # Numero di notti di osservazione
t_max = 20.0        # Finestra temporale totale [giorni]

# Tempi di osservazione non perfettamente equispaziati (più realistici)
t_dati = np.sort(np.random.uniform(0, t_max, N_misure))

# Curva teorica esatta nei punti osservati
v_teorica = v_radiale_fit(t_dati, A_vero, w_vero, phi_vero)

# Aggiunta di rumore gaussiano (incertezza dello spettrografo, es. 12 m/s)
errore_spettrografo = 12.0
v_err = np.full(N_misure, errore_spettrografo)
rumore = np.random.normal(0, errore_spettrografo, size=N_misure)
v_misurata = v_teorica + rumore

# 3. Fit dei dati simulati
# Stima iniziale p0 = [A, w, phi] (fondamentale per far convergere il coseno)
A_init = 0.5 * (np.max(v_misurata) - np.min(v_misurata))
P_init = 4.0
w_init = 2 * np.pi / P_init
phi_init = 0.0
p0 = [A_init, w_init, phi_init]

par, pcov = optimize.curve_fit(
    v_radiale_fit, t_dati, v_misurata,
    p0=p0, sigma=v_err, absolute_sigma=True
)
perr = np.sqrt(np.diag(pcov))

# Ricavo il periodo dal fit: P = 2*pi / w (con propagazione dell'errore)
P_fit = 2 * np.pi / par[1]
P_err = (2 * np.pi / (par[1] ** 2)) * perr[1]

# Calcolo Chi-quadro ridotto
residui = v_misurata - v_radiale_fit(t_dati, *par)
chi2 = np.sum((residui / v_err) ** 2)
ndf = N_misure - len(par)
chi2_rid = chi2 / ndf

# 4. Stampa risultati a confronto con i valori veri
print("=== CONFRONTO PARAMETRI ===")
print(f"Ampiezza A : vero = {A_vero:.2f} m/s   | fit = {par[0]:.2f} ± {perr[0]:.2f} m/s")
print(f"Periodo  P : vero = {P_vero:.3f} gg    | fit = {P_fit:.3f} ± {P_err:.3f} gg")
print(f"Fase   phi : vero = {phi_vero:.2f} rad   | fit = {par[2]:.2f} ± {perr[2]:.2f} rad")
print(f"Chi2 / ndf = {chi2_rid:.2f}")

# 5. Grafico di confronto
t_plot = np.linspace(0, t_max, 1000)

plt.figure(figsize=(10, 6))
plt.errorbar(t_dati, v_misurata, yerr=v_err, fmt='o', color='#983232', label='Dati simulati (con rumore)')
plt.plot(t_plot, v_radiale_fit(t_plot, A_vero, w_vero, phi_vero), '--', color='gray', linewidth=1.5, label='Segnale vero (senza rumore)')
plt.plot(t_plot, v_radiale_fit(t_plot, *par), '-', color='#1b92cd', linewidth=2, label='Fit $A\\cos(\\omega t + \\phi)$')

plt.axhline(0, color='black', linestyle=':', alpha=0.5)
plt.xlabel('Tempo [giorni]')
plt.ylabel('Velocità radiale [m/s]')
plt.title(f'Simulazione scoperta esopianeta: $A = {par[0]:.1f} \\pm {perr[0]:.1f}$ m/s, $P = {P_fit:.2f} \\pm {P_err:.2f}$ gg')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('simulazione_esopianeta.png', bbox_inches='tight')
plt.show()