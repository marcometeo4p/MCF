import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def f_g1(x, A, mu, sigma, m, q):
    """
    Funzione di fit: Gaussiana + polinomio di primo grado (retta).
    
    Parametri:
    - x: variabile indipendente (es. massa invariante)
    - A: ampiezza (altezza) del picco gaussiano
    - mu: media (posizione centrale del picco)
    - sigma: deviazione standard (larghezza del picco)
    - m: coefficiente angolare del fondo lineare
    - q: intercetta del fondo lineare
    """
    gauss = A * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    poly1 = m * x + q
    return gauss + poly1

def f_g2(x, A1, A2, mu, sigma1, sigma2, m, q):
    """
    Funzione di fit: Doppia Gaussiana (con media condivisa) + polinomio di primo grado (retta).
    
    Parametri:
    - x: variabile indipendente (es. massa invariante)
    - A1: ampiezza (altezza) della prima gaussiana
    - A2: ampiezza (altezza) della seconda gaussiana
    - mu: media condivisa (posizione centrale dei due picchi)
    - sigma1: deviazione standard (larghezza) della prima gaussiana
    - sigma2: deviazione standard (larghezza) della seconda gaussiana
    - m: coefficiente angolare del fondo lineare
    - q: intercetta del fondo lineare
    """
    gauss1 = A1 * np.exp(-0.5 * ((x - mu) / sigma1) ** 2)
    gauss2 = A2 * np.exp(-0.5 * ((x - mu) / sigma2) ** 2)
    poly1 = m * x + q
    return gauss1 + gauss2 + poly1


dataset = pd.read_csv('http://opendata.cern.ch/record/5203/files/Jpsimumu.csv')
dataset['massa_invariante']=np.sqrt((dataset['E1']+dataset['E2'])**2-((dataset['px1']+dataset['px2'])**2+(dataset['py1']+dataset['py2'])**2+(dataset['pz1']+dataset['pz2'])**2))
'''
plt.figure(figsize=(10,8))
plt.hist(dataset['massa_invariante'],bins=150,color='orange',label='massa_invariante')
plt.legend()
plt.xlabel('valore')
plt.xlabel('valore [GeV/c²]')
plt.savefig('m_inv.png')
plt.close()

ds = dataset[dataset['massa_invariante'].between(2.85, 3.35)]

plt.figure(figsize=(10, 8))
plt.hist(ds['massa_invariante'], bins=70, color="#1b92cd", label='massa_invariante')
plt.legend()
plt.xlabel('valore [GeV/c²]')
plt.ylabel('num eventi')
plt.savefig('m_inv_zoom.png', bbox_inches='tight')
plt.close()
'''
ds=dataset
# 1. Estrazione dei dati dall'istogramma
counts_raw, bin_edges = np.histogram(ds['massa_invariante'], bins=400)
bin_centers_raw = 0.5 * (bin_edges[:-1] + bin_edges[1:])

# FILTRO BIN VUOTI: evita divisione per zero (y_err = 0) in curve_fit e nei pull
mask = counts_raw > 0
bin_centers = bin_centers_raw[mask]
counts = counts_raw[mask]
y_err = np.sqrt(counts)

# Stima parametri iniziali p0 = [A, mu, sigma, m, q] per garantire la convergenza
p0 = [np.max(counts) - np.min(counts), bin_centers[np.argmax(counts)], 0.03, 0.0, np.min(counts)]

# 2. Fit con curve_fit
par, pc = optimize.curve_fit(f_g1, bin_centers, counts, p0=p0, sigma=y_err, absolute_sigma=True)
perr = np.sqrt(np.diag(pc))
print(par,perr)

'''plt.figure(figsize=(10, 8))
plt.errorbar(bin_centers, counts,yerr=y_err, fmt='.',color="#983232", alpha=0.6, label='Dati (massa invariante)')

x_plot = np.linspace(bin_edges[0], bin_edges[-1], 1000)
plt.plot(x_plot, f_g1(x_plot, *par), color='orange', linewidth=2, label='Fit $f_{g1}$ (Gauss + Pol1)')
plt.plot(x_plot, par[3]*x_plot + par[4], color='blue', linestyle='--', label='Fondo lineare ($mx + q$)')

plt.xlabel('Massa invariante [GeV/c²]')
plt.ylabel('Numero eventi')
plt.title(f'Fit J/ψ: $\mu = {par[1]:.4f} \pm {perr[1]:.4f}$ GeV/c²')
plt.legend()
plt.grid(True, alpha=0.4)
plt.savefig('m_inv_fit_tutto.png', bbox_inches='tight')
plt.close()'''



# 3. Calcolo valori attesi, scarti e Chi-quadro
y_fit = f_g1(bin_centers, *par)
scarti = counts - y_fit                  # Scarto: dati - fit
scarti_norm = scarti / y_err             # Pull: (dati - fit) / errore

chi2 = np.sum(scarti_norm ** 2)
ndf = len(counts) - len(par)             # Gradi di libertà (N_bin - N_parametri)
chi2_rid = chi2 / ndf

# 4. Costruzione del testo dei risultati, stampa e salvataggio su file .txt
nomi_param = ['A', 'mu', 'sigma', 'm', 'q']

righe = ["=== RISULTATI DEL FIT (f_g1) ==="]
for nome, val, err in zip(nomi_param, par, perr):
    righe.append(f"{nome:6s} = {val:.5f} ± {err:.5f}")

righe.append("-" * 32)
righe.append(f"Chi2       = {chi2:.2f}")
righe.append(f"ndf        = {ndf}")
righe.append(f"Chi2 / ndf = {chi2_rid:.3f}")

# Unisce tutte le righe in un'unica stringa separata da a-capo
testo_risultati = "\n".join(righe)

# Stampa a schermo
print(testo_risultati)

# Salva nel file .txt
with open("risultati_fit_g1_tutto.txt", "w", encoding="utf-8") as file_out:
    file_out.write(testo_risultati)

# 5. Grafico a 3 pannelli (Dati+Fit, Scarti, Scarti normalizzati)
fig, (ax1, ax2, ax3) = plt.subplots(
    3, 1, 
    figsize=(10, 11), 
    sharex=True, 
    gridspec_kw={'height_ratios':[2,1,1], 'hspace': 0.08}
)

# --- PANNELLO 1: Dati e Fit ---
ax1.errorbar(bin_centers, counts, yerr=y_err, fmt='.', color="#983232", alpha=0.7, label='Dati (massa invariante)')
x_plot = np.linspace(bin_edges[0], bin_edges[-1], 1000)
ax1.plot(x_plot, f_g1(x_plot, *par), color='orange', linewidth=2, label='Fit $f_{g1}$ (Gauss + Pol1)')
ax1.plot(x_plot, par[3]*x_plot + par[4], color='blue', linestyle='--', label='Fondo lineare ($mx + q$)')
ax1.set_ylabel('Numero eventi')
ax1.set_title(f'Fit J/ψ: $\mu = {par[1]:.4f} \pm {perr[1]:.4f}$ GeV/c²  |  $\chi^2/ndf = {chi2_rid:.2f}$')
ax1.legend()
ax1.grid(True, alpha=0.4)

# --- PANNELLO 2: Scarto (Dati - Fit) ---
ax2.errorbar(bin_centers, scarti, yerr=y_err, fmt='.', color="#983232", alpha=0.7)
ax2.axhline(0, color='orange', linestyle='-', linewidth=1.5)
ax2.set_ylabel('Dati - Fit')
ax2.grid(True, alpha=0.4)

# --- PANNELLO 3: Scarto normalizzato ((Dati - Fit) / Errore) ---
ax3.errorbar(bin_centers, scarti_norm, yerr=1.0, fmt='.', color="#983232", alpha=0.7)
ax3.axhline(0, color='orange', linestyle='-', linewidth=1.5)
ax3.axhline(1, color='gray', linestyle=':', linewidth=1)
ax3.axhline(-1, color='gray', linestyle=':', linewidth=1)
ax3.set_ylabel('Pull $\\frac{\\text{Dati - Fit}}{\\sigma}$')
ax3.set_xlabel('Massa invariante [GeV/c²]')
ax3.set_ylim(-4, 4)  # Fissa una scala leggibile per i pull (solitamente tra -3 e +3)
ax3.grid(True, alpha=0.4)
plt.savefig('m_inv_fit_g1_completo_tutto.png', bbox_inches='tight')
plt.close()



#=========================fit2=================================
# Stima parametri iniziali p0_2 = [A1, A2, mu, sigma1, sigma2, m, q]
A_tot = np.max(counts) - np.min(counts)
mu_init = bin_centers[np.argmax(counts)]
q_init = np.min(counts)
p0_2 = [0.7 * A_tot, 0.3 * A_tot, mu_init, 0.02, 0.05, 0.0, q_init]

# 2. Fit con curve_fit usando f_g2
par2, pc2 = optimize.curve_fit(f_g2, bin_centers, counts, p0=p0_2, sigma=y_err, absolute_sigma=True)
perr2 = np.sqrt(np.diag(pc2))

'''plt.figure(figsize=(10, 8))
plt.errorbar(bin_centers, counts,yerr=y_err, fmt='.',color="#983232", alpha=0.6, label='Dati (massa invariante)')

x_plot = np.linspace(bin_edges[0], bin_edges[-1], 1000)
plt.plot(x_plot, f_g2(x_plot, *par2), color='orange', linewidth=2, label='Fit $f_{g2}$ (Gauss1 + Gauss2 + Pol1)')
plt.plot(x_plot, par2[3]*x_plot + par2[4], color='blue', linestyle='--', label='Fondo lineare ($mx + q$)')

plt.xlabel('Massa invariante [GeV/c²]')
plt.ylabel('Numero eventi')
plt.title(f'Fit J/ψ: $\mu = {par2[1]:.4f} \pm {perr2[1]:.4f}$ GeV/c²')
plt.legend()
plt.grid(True, alpha=0.4)

plt.savefig('m_inv_fit2_tutto.png', bbox_inches='tight')
plt.close()'''

# 3. Calcolo valori attesi, scarti e Chi-quadro
y_fit2 = f_g2(bin_centers, *par2)
scarti2 = counts - y_fit2                 # Scarto: dati - fit
scarti_norm2 = scarti2 / y_err            # Pull: (dati - fit) / errore

chi2_2 = np.sum(scarti_norm2 ** 2)
ndf_2 = len(counts) - len(par2)           # Gradi di libertà (150 - 7 = 143)
chi2_rid2 = chi2_2 / ndf_2

# 4. Costruzione del testo dei risultati, stampa e salvataggio su file .txt
nomi_param2 = ['A1', 'A2', 'mu', 'sigma1', 'sigma2', 'm', 'q']

righe2 = ["=== RISULTATI DEL FIT (f_g2) ==="]
for nome, val, err in zip(nomi_param2, par2, perr2):
    righe2.append(f"{nome:6s} = {val:.5f} ± {err:.5f}")

righe2.append("-" * 32)
righe2.append(f"Chi2       = {chi2_2:.2f}")
righe2.append(f"ndf        = {ndf_2}")
righe2.append(f"Chi2 / ndf = {chi2_rid2:.3f}")

testo_risultati2 = "\n".join(righe2)

# Stampa a schermo
print(testo_risultati2)

# Salva nel file .txt dedicato a f_g2
with open("risultati_fit_g2_tutto.txt", "w", encoding="utf-8") as file_out:
    file_out.write(testo_risultati2)

# 5. Grafico a 3 pannelli (Dati+Fit, Scarti, Scarti normalizzati)
fig, (ax1, ax2, ax3) = plt.subplots(
    3, 1, 
    figsize=(10, 11), 
    sharex=True, 
    gridspec_kw={'height_ratios':[2,1,1], 'hspace': 0.08}
)

# Calcolo delle componenti singole su x_plot per visualizzarle nel grafico
x_plot = np.linspace(bin_edges[0], bin_edges[-1], 1000)
fondo_plot = par2[5] * x_plot + par2[6]
gaus1_plot = par2[0] * np.exp(-0.5 * ((x_plot - par2[2]) / par2[3]) ** 2)
gaus2_plot = par2[1] * np.exp(-0.5 * ((x_plot - par2[2]) / par2[4]) ** 2)

# --- PANNELLO 1: Dati e Fit ---
ax1.errorbar(bin_centers, counts, yerr=y_err, fmt='.', color="#983232", alpha=0.7, label='Dati (massa invariante)')
ax1.plot(x_plot, f_g2(x_plot, *par2), color='orange', linewidth=2.2, label='Fit $f_{g2}$ (Doppia Gauss + Pol1)')
ax1.plot(x_plot, fondo_plot, color='blue', linestyle='--', label='Fondo lineare ($mx + q$)')
ax1.plot(x_plot, gaus1_plot, color='green', linestyle=':', linewidth=1.5, label='Gaussiana 1 ($A_1, \\sigma_1$)')
ax1.plot(x_plot, gaus2_plot, color='purple', linestyle='-.', linewidth=1.5, label='Gaussiana 2 ($A_2, \\sigma_2$)')

ax1.set_ylabel('Numero eventi')
ax1.set_title(f'Fit J/ψ ($f_{{g2}}$): $\\mu = {par2[2]:.4f} \\pm {perr2[2]:.4f}$ GeV/c²  |  $\\chi^2/ndf = {chi2_rid2:.2f}$')
ax1.legend()
ax1.grid(True, alpha=0.4)

# --- PANNELLO 2: Scarto (Dati - Fit) ---
ax2.errorbar(bin_centers, scarti2, yerr=y_err, fmt='.', color="#983232", alpha=0.7)
ax2.axhline(0, color='orange', linestyle='-', linewidth=1.5)
ax2.set_ylabel('Dati - Fit')
ax2.grid(True, alpha=0.4)

# --- PANNELLO 3: Scarto normalizzato ((Dati - Fit) / Errore) ---
ax3.errorbar(bin_centers, scarti_norm2, yerr=1.0, fmt='.', color="#983232", alpha=0.7)
ax3.axhline(0, color='orange', linestyle='-', linewidth=1.5)
ax3.axhline(1, color='gray', linestyle=':', linewidth=1)
ax3.axhline(-1, color='gray', linestyle=':', linewidth=1)
ax3.set_ylabel('Pull $\\frac{\\text{Dati - Fit}}{\\sigma}$')
ax3.set_xlabel('Massa invariante [GeV/c²]')
ax3.set_ylim(-4, 4)
ax3.grid(True, alpha=0.4)

plt.savefig('m_inv_fit_g2_completo_tutto.png', bbox_inches='tight')
plt.close()