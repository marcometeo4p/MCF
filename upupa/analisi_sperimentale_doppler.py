import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize, signal


def modello_rv(t: np.ndarray, A: float, w: float, phi: float) -> np.ndarray:
    """Modello fisico della velocità radiale: v_r(t) = A * cos(w * t + phi)."""
    return A * np.cos(w * t + phi)


def simula_osservazioni(
    t_sorgente: np.ndarray,
    v_sorgente: np.ndarray,
    n_misure: int,
    errore_strumentale: float,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Campiona una curva continua (analitica o da simulazione N-body) in istanti
    casuali e aggiunge rumore gaussiano strumentale.
    """
    rng = np.random.default_rng(seed)

    # Estrazione di istanti osservativi non equispaziati nell'intervallo disponibile
    t_min, t_max = np.min(t_sorgente), np.max(t_sorgente)
    t_dati = np.sort(rng.uniform(t_min, t_max, size=n_misure))

    # Interpolazione del segnale pulito nei tempi di osservazione
    v_pulita = np.interp(t_dati, t_sorgente, v_sorgente)

    # Aggiunta rumore gaussiano
    v_err = np.full(n_misure, errore_strumentale)
    v_misurata = v_pulita + rng.normal(0.0, errore_strumentale, size=n_misure)

    return t_dati, v_misurata, v_err


def stima_parametri_iniziali(t_dati: np.ndarray, v_dati: np.ndarray) -> list[float]:
    """
    Stima automaticamente [A, w, phi] tramite periodogramma di Lomb-Scargle
    e proiezione lineare di fase, evitando minimi locali nel fit.
    """
    t_span = np.max(t_dati) - np.min(t_dati)
    dt_mediano = np.median(np.diff(t_dati))

    # Griglia di pulsazioni angolari w [rad / unità_tempo]
    w_min = 2 * np.pi / (2.0 * t_span)
    w_max = np.pi / max(dt_mediano, 1e-4)
    w_grid = np.linspace(w_min, w_max, 5000)

    # Periodogramma di Lomb-Scargle (gestisce campionamenti irregolari)
    pgram = signal.lombscargle(t_dati, v_dati - np.mean(v_dati), w_grid)
    w_init = w_grid[np.argmax(pgram)]

    # Stima analitica di A e phi fissata w_init: A*cos(wt + phi) = c1*cos(wt) - c2*sin(wt)
    X = np.column_stack([np.cos(w_init * t_dati), -np.sin(w_init * t_dati)])
    coeff, _, _, _ = np.linalg.lstsq(X, v_dati, rcond=None)
    A_init = float(np.hypot(coeff[0], coeff[1]))
    phi_init = float(np.arctan2(coeff[1], coeff[0]))

    return [A_init, w_init, phi_init]


def fit_velocita_radiale(
    t_dati: np.ndarray,
    v_dati: np.ndarray,
    v_err: np.ndarray,
    p0: list[float] | None = None,
) -> dict:
    """
    Esegue il fit ai minimi quadrati pesati su v_r(t) e restituisce un dizionario
    con parametri, incertezze, periodo, significatività SNR e chi-quadro ridotto.
    """
    if p0 is None:
        p0 = stima_parametri_iniziali(t_dati, v_dati)

    par, pcov = optimize.curve_fit(
        modello_rv, t_dati, v_dati,
        p0=p0, sigma=v_err, absolute_sigma=True, maxfev=10000
    )
    perr = np.sqrt(np.diag(pcov))

    # Normalizza A > 0 se il fit converge su ampiezza negativa
    if par[0] < 0:
        par[0] = -par[0]
        par[2] = (par[2] + np.pi) % (2 * np.pi)

    # Periodo e propagazione dell'errore: P = 2*pi / w
    P_fit = 2 * np.pi / par[1]
    P_err = (2 * np.pi / (par[1] ** 2)) * perr[1]

    # Residui e Chi-quadro ridotto
    residui = v_dati - modello_rv(t_dati, *par)
    chi2 = np.sum((residui / v_err) ** 2)
    ndf = max(1, len(t_dati) - len(par))
    chi2_rid = chi2 / ndf

    return {
        "par": par,
        "perr": perr,
        "A": par[0], "A_err": perr[0],
        "w": par[1], "w_err": perr[1],
        "phi": par[2], "phi_err": perr[2],
        "P": P_fit, "P_err": P_err,
        "snr": par[0] / perr[0],       # Significatività della rivelazione (in sigma)
        "chi2_rid": chi2_rid,
        "residui": residui,
    }


def stampa_report_fit(risultati: dict, parametri_veri: dict | None = None) -> None:
    """Stampa i risultati del fit confrontandoli (se disponibili) con i valori veri."""
    print("=== RISULTATI FIT DOPPLER ===")
    if parametri_veri:
        print(f"Ampiezza A : vero = {parametri_veri['A']:.2f} m/s   | fit = {risultati['A']:.2f} ± {risultati['A_err']:.2f} m/s")
        print(f"Periodo  P : vero = {parametri_veri['P']:.3f} gg    | fit = {risultati['P']:.3f} ± {risultati['P_err']:.3f} gg")
        print(f"Fase   phi : vero = {parametri_veri['phi']:.2f} rad   | fit = {risultati['phi']:.2f} ± {risultati['phi_err']:.2f} rad")
    else:
        print(f"Ampiezza A : {risultati['A']:.2f} ± {risultati['A_err']:.2f} m/s (Significatività: {risultati['snr']:.1f} σ)")
        print(f"Periodo  P : {risultati['P']:.3f} ± {risultati['P_err']:.3f} unità tempo")
        print(f"Fase   phi : {risultati['phi']:.2f} ± {risultati['phi_err']:.2f} rad")
    print(f"Chi2 / ndf = {risultati['chi2_rid']:.2f}\n")


def plot_fit_doppler(
    t_dati: np.ndarray,
    v_dati: np.ndarray,
    v_err: np.ndarray,
    risultati: dict,
    curva_vera: tuple[np.ndarray, np.ndarray] | None = None,
    unita_tempo: str = "giorni",
    save_path: str | None = None,
) -> None:
    """Genera il grafico del fit con pannello inferiore dei residui."""
    t_plot = np.linspace(np.min(t_dati), np.max(t_dati), 1000)

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
    )

    # Pannello superiore: dati e modelli
    ax1.errorbar(t_dati, v_dati, yerr=v_err, fmt="o", color="#983232", label="Dati simulati (con rumore)")
    if curva_vera is not None:
        ax1.plot(curva_vera[0], curva_vera[1], "--", color="gray", linewidth=1.5, label="Segnale vero (senza rumore)")
    ax1.plot(t_plot, modello_rv(t_plot, *risultati["par"]), "-", color="#1b92cd", linewidth=2, label="Fit $A\\cos(\\omega t + \\phi)$")

    ax1.axhline(0, color="black", linestyle=":", alpha=0.5)
    ax1.set_ylabel("Velocità radiale [m/s]")
    ax1.set_title(
        f"Fit Doppler: $A = {risultati['A']:.1f} \\pm {risultati['A_err']:.1f}$ m/s, "
        f"$P = {risultati['P']:.2f} \\pm {risultati['P_err']:.2f}$ {unita_tempo} "
        f"($\\chi^2_{{\\nu}} = {risultati['chi2_rid']:.2f}$)"
    )
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Pannello inferiore: residui
    ax2.errorbar(t_dati, risultati["residui"], yerr=v_err, fmt="o", color="#983232", alpha=0.8)
    ax2.axhline(0, color="#1b92cd", linestyle="-", linewidth=1.5)
    ax2.set_xlabel(f"Tempo [{unita_tempo}]")
    ax2.set_ylabel("Residui [m/s]")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches="tight", dpi=150)
    plt.show()