'''def parse_arguments():
    
    parser = arg.ArgumentParser(description='Esempio utilizzo argarse.',usage='python3 argparse_example.py  --opzione')
    parser.add_argument('-p1',    action='store_true', default=False, help='visualizza risoluzione per il potenziale 1')
    parser.add_argument('-p2',    action='store_true', default=False, help='visualizza risoluzione per il potenziale 2')
    parser.add_argument('-p3',    action='store_true', default=False, help='visualizza risoluzione per il potenziale 3')
    parser.add_argument('-p4',    action='store_true', default=False, help='visualizza risoluzione per il potenziale 4')
    parser.add_argument('-m', default=1, help='inserisce il valore della massa del corpo, dafault =1')
    return  parser.parse_args()'''
import argparse
from genericpath import exists
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson


# Definizione dei potenziali simmetrici V(x) e delle rispettive derivate prime V'(x)
POTENZIALI = {
    "armonico": {
        "label": r"$V_a(x) = k x^2$ (Armonico)",
        "V": lambda x, k: k * x**2,
        "dV": lambda x, k: 2 * k * x,
    },
    "quartico": {
        "label": r"$V(x) = k x^4$ (Quartico)",
        "V": lambda x, k: k * x**4,
        "dV": lambda x, k: 4 * k * x**3,
    },
    "frazionario": {
        "label": r"$V(x) = k |x|^{3/2}$",
        "V": lambda x, k: k * np.abs(x) ** 1.5,
        "dV": lambda x, k: 1.5 * k * np.sqrt(np.abs(x)) * np.sign(x),
    },
    "sestico": {
        "label": r"$V(x) = k x^6$ (Sestico)",
        "V": lambda x, k: k * x**6,
        "dV": lambda x, k: 6 * k * x**5,
    },
}


def calcola_periodo(x0, m, k, V_func, dV_func, n_punti=10001):
    """
    Calcola T(x0) tramite scipy.integrate.simpson con correzione analitica
    per la singolarità integrabile in x = x0.
    """
    eps = 1e-7 * x0
    x = np.linspace(0.0, x0 - eps, n_punti)

    V_x0 = V_func(x0, k)
    V_x = V_func(x, k)
    integranda = 1.0 / np.sqrt(V_x0 - V_x)

    # Integrale numerico su [0, x0 - eps] con regola di Simpson
    integrale_num = simpson(integranda, x=x)

    # Contributo residuo su [x0 - eps, x0]
    dV_x0 = dV_func(x0, k)
    coda_analitica = 2.0 * np.sqrt(eps / dV_x0) if dV_x0 > 0 else 0.0

    return np.sqrt(8.0 * m) * (integrale_num + coda_analitica)


def parse_args():
    parser = argparse.ArgumentParser( description="Calcolo e grafico del periodo T(x0) per potenziali 1D simmetrici.")
    parser.add_argument(
        "-p",
        "--potenziali",
        nargs="+",
        choices=list(POTENZIALI.keys()) + ["tutti"],
        default=["tutti"],
        help="Potenziali da visualizzare (default: tutti).",)
    parser.add_argument("-m", "--massa", type=float, default=1.0, help="Massa della particella in kg (default: 1.0).")
    parser.add_argument("-k", type=float, default=1.0, help="Costante k del potenziale (default: 1.0).")
    parser.add_argument(
        "--xmin", type=float, default=0.1, help="Valore minimo di x0 (default: 0.1).")
    parser.add_argument(
        "--xmax", type=float, default=3.0, help="Valore massimo di x0 (default: 3.0).")
    parser.add_argument(
        "--punti-x0", type=int, default=150, help="Numero di punti per x0 (default: 150).")
    parser.add_argument(
        "--log", action="store_true", help="Usa scala logaritmica su entrambi gli assi.")
    return parser.parse_args()



args = parse_args()
args.costante = args.k

if "tutti" in args.potenziali:
    scelti = list(POTENZIALI.keys())
else:
    scelti = list(dict.fromkeys(args.potenziali))  # Rimuove eventuali duplicati

x0_vals = np.linspace(args.xmin, args.xmax, args.punti_x0)

plt.figure(figsize=(15, 10))
risultati = {}
for nome in scelti:
    info = POTENZIALI[nome]
    T_vals = np.array(
        [calcola_periodo(x0, args.massa, args.costante, info["V"], info["dV"]) for x0 in x0_vals]
    )
    risultati[nome] = T_vals
    plt.plot(x0_vals, T_vals, linewidth=2, label=info["label"])

    # Se è presente l'armonico, mostra anche il valore teorico T = 2*pi*sqrt(m / (2k))
    if nome == "armonico":
        T_teorico = 2.0 * np.pi * np.sqrt(args.massa / (2.0 * args.costante))
        errore_max = np.max(np.abs(T_vals - T_teorico))
        print(f"[Armonico] T teorico = {T_teorico:.8f} s | Errore max Simpson = {errore_max:.2e} s")
        plt.axhline(
            T_teorico,
            color="black",
            linestyle="--",
            alpha=0.6,
            label=rf"Teorico armonico ($2\pi\sqrt{{m/2k}} \approx {T_teorico:.3f}$ s)",
        )

if args.log:
    plt.xscale("log")
    plt.yscale("log")
plt.title(f"Periodo di oscillazione $T(x_0)$  ($m = {args.massa}$, $k = {args.costante}$)")
plt.xlabel(r"Ampiezza iniziale $x_0$ [m]")
plt.ylabel(r"Periodo $T(x_0)$ [s]")
plt.grid(True, which="both", linestyle=":", alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('garfico_tutto.png')
plt.show()

# Ciclo per i singoli grafici
for i, chiave in enumerate(scelti):
        plt.figure(figsize=(12, 8))
        info = POTENZIALI[chiave]
        T_vals = risultanze_tse = risultati[chiave] if chiave in risultati else np.array([]) # corretto qui sotto semplicemente come risultati[chiave]
        T_vals = risultati[chiave]

        plt.plot(x0_vals, T_vals, linewidth=2, color=f"C{i}", label=info["label"])
        
        # Corretto il controllo su "armonico" anziché "p1" e args.massa anziché args.m
        if chiave == "armonico":
            T_teorico = 2.0 * np.pi * np.sqrt(args.massa / (2.0 * args.costante))
            plt.axhline(
                T_teorico,
                color="black",
                linestyle="--",
                alpha=0.6,
                label=rf"Teorico ($\approx {T_teorico:.3f}$ s)",
            )
        if args.log:
            plt.xscale("log")
            plt.yscale("log")
        plt.title(f"Confronto singolo per potenziale ($m = {args.massa}$, $k = {args.costante}$)---> {chiave}", fontsize=13)
        plt.xlabel(r"Ampiezza iniziale $x_0$ [m]")
        plt.ylabel(r"Periodo $T(x_0)$ [s]")
        plt.grid(True, which="both", linestyle=":", alpha=0.7)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'garfico_{chiave}.png')
        plt.show()
        '''if args.log:
            ax.set_xscale("log")
            ax.set_yscale("log")

        ax.set_title(info["label"])
        ax.set_xlabel(r"Ampiezza iniziale $x_0$ [m]")
        ax.set_ylabel(r"Periodo $T(x_0)$ [s]")
        ax.grid(True, which="both", linestyle=":", alpha=0.7)
        ax.legend()

fig.suptitle(f"Confronto singolo per potenziale ($m = {args.massa}$, $k = {args.k}$)", fontsize=13)
plt.tight_layout()
plt.savefig("grafico_singoli.png")
plt.show()'''
