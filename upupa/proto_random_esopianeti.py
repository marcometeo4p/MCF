import numpy as np
import matplotlib.pyplot as plt

# Costanti di conversione in unità astronomiche (AU, M_sun, yr)
G_AU = 4 * np.pi**2                 # AU^3 / (M_sun * yr^2)
AU_YR_TO_MS = 4740.470463533348     # 1 AU/yr in m/s
M_EARTH_TO_MSUN = 3.003489e-6       # Massa terrestre in M_sun
M_JUP_TO_MSUN = 9.547919e-4         # Massa gioviana in M_sun


def compute_rv_semi_amplitude(
    m_planet: np.ndarray,
    a: np.ndarray,
    e: np.ndarray,
    sin_i: np.ndarray,
    m_star: float = 1.0,
) -> np.ndarray:
    """Calcola la semiampiezza K (in m/s) della velocità radiale stellare."""
    k_au_yr = (
        np.sqrt(G_AU / (a * (1.0 - e**2)))
        * (m_planet * sin_i)
        / np.sqrt(m_star + m_planet)
    )
    return k_au_yr * AU_YR_TO_MS


def run_detectability_mc(
    n_samples: int = 200_000,
    m_star: float = 1.0,
    seed: int = 42,
    save_plot: str = "rv_completeness_map.png",
):
    rng = np.random.default_rng(seed)

    # 1. Campionamento dei prior astrofisici
    # Masse pianeti: log-uniforme da 0.5 M_Terra a 10 M_Giove
    log_m_min = np.log10(0.5 * M_EARTH_TO_MSUN)
    log_m_max = np.log10(10.0 * M_JUP_TO_MSUN)
    m_planet = 10 ** rng.uniform(log_m_min, log_m_max, size=n_samples)

    # Semiasse maggiore: log-uniforme da 0.05 AU a 10 AU
    a = 10 ** rng.uniform(np.log10(0.05), np.log10(10.0), size=n_samples)

    # Inclinazione isotropa in 3D: cos(i) uniforme in [0, 1]
    cos_i = rng.uniform(0.0, 1.0, size=n_samples)
    sin_i = np.sqrt(1.0 - cos_i**2)

    # Eccentricità: distribuzione Beta ispirata agli esopianeti osservati (Kipping 2013)
    e = rng.beta(0.867, 3.03, size=n_samples)

    # 2. Calcolo del segnale Doppler K (m/s)
    K = compute_rv_semi_amplitude(m_planet, a, e, sin_i, m_star=m_star)

    # 3. Soglie strumentali (criterio di rilevazione 3-sigma: K > 3 * sigma_strumentale)
    instruments = {
        "Prima gen. (K > 30 m/s)": 30.0,
        "Classe HARPS (K > 3 m/s)": 3.0,
        "Classe ESPRESSO (K > 0.3 m/s)": 0.3,
    }

    print(f"--- Monte Carlo RV Completeness ({n_samples:,} sistemi, M_star = {m_star} M_sun) ---")
    for name, threshold in instruments.items():
        frac = np.mean(K > threshold) * 100
        print(f"{name:<32}: {frac:5.1f}% dei sistemi rilevabili")

    # 4. Generazione Heatmap (Probabilità di rilevazione con soglia classe HARPS: K > 3 m/s)
    k_threshold = 3.0
    detected = (K > k_threshold).astype(float)

    m_earth_units = m_planet / M_EARTH_TO_MSUN
    bins_a = np.logspace(np.log10(0.05), np.log10(10.0), 35)
    bins_m = np.logspace(np.log10(0.5), np.log10(10.0 * M_JUP_TO_MSUN / M_EARTH_TO_MSUN), 35)

    total_hist, _, _ = np.histogram2d(a, m_earth_units, bins=[bins_a, bins_m])
    det_hist, _, _ = np.histogram2d(a, m_earth_units, bins=[bins_a, bins_m], weights=detected)

    # Probabilità per cella (evitando divisioni per zero)
    prob_map = np.divide(det_hist, total_hist, out=np.zeros_like(det_hist), where=total_hist > 0)

    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=150)
    mesh = ax.pcolormesh(bins_a, bins_m, prob_map.T * 100, cmap="viridis", shading="auto", vmin=0, vmax=100)
    cbar = plt.colorbar(mesh, ax=ax, label="Probabilità di rilevazione (%)")

    # Riferimenti del Sistema Solare e Hot Jupiter
    references = [
        ("Terra", 1.0, 1.0),
        ("Nettuno", 30.07, 17.15),
        ("Giove", 5.20, 317.8),
        ("Hot Jupiter", 0.05, 317.8),
    ]
    for label, ref_a, ref_m in references:
        if 0.05 <= ref_a <= 10.0:
            ax.scatter(ref_a, ref_m, color="white", edgecolor="black", s=60, zorder=5)
            ax.annotate(
                label,
                (ref_a, ref_m),
                textcoords="offset points",
                xytext=(6, 4),
                color="white",
                fontweight="bold",
                fontsize=9,
            )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Semiasse maggiore $a$ [AU]")
    ax.set_ylabel("Massa planetaria $m_p$ [$M_\\oplus$]")
    ax.set_title(f"Completezza Spettroscopia Doppler (Soglia $K > {k_threshold}$ m/s, $M_\\star = {m_star}\\,M_\\odot$)")
    plt.tight_layout()
    plt.savefig(save_plot)
    print(f"\nGrafico salvato in: {save_plot}")


if __name__ == "__main__":
    run_detectability_mc()