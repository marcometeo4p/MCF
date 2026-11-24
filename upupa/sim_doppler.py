import numpy as np
from analisi_sperimentale_doppler import (
    modello_rv,
    simula_osservazioni,
    fit_velocita_radiale,
    stampa_report_fit,
    plot_fit_doppler,
)

# --- SCENARIO A: Test analitico (il tuo caso attuale) ---
A_vero, P_vero, phi_vero = 55.0, 4.2, 0.8
w_vero = 2 * np.pi / P_vero

t_griglia = np.linspace(0, 20.0, 2000)
v_griglia = modello_rv(t_griglia, A_vero, w_vero, phi_vero)

t_dati, v_mis, v_err = simula_osservazioni(
    t_griglia, v_griglia, n_misure=45, errore_strumentale=12.0, seed=42
)

risultati = fit_velocita_radiale(t_dati, v_mis, v_err)
stampa_report_fit(risultati, parametri_veri={"A": A_vero, "P": P_vero, "phi": phi_vero})
plot_fit_doppler(
    t_dati, v_mis, v_err, risultati,
    curva_vera=(t_griglia, v_griglia),
    save_path="simulazione_esopianeta.png",
)

# --- SCENARIO B: Collegamento diretto al simulatore N-body ---
# Una volta eseguita sistema.simulate(t_max, dt):
#
# t_nbody = sistema.history_t * 365.25                 # conversione anni -> giorni
# v_nbody = sistema.get_radial_velocity(star_index=0)  # in m/s
#
# t_dati, v_mis, v_err = simula_osservazioni(t_nbody, v_nbody, n_misure=50, errore_strumentale=5.0)
# risultati_nbody = fit_velocita_radiale(t_dati, v_mis, v_err)
# stampa_report_fit(risultati_nbody)
# plot_fit_doppler(t_dati, v_mis, v_err, risultati_nbody, curva_vera=(t_nbody, v_nbody))