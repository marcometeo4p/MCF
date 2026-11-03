import pandas as pd
import matplotlib.pyplot as plt

dati=pd.read_csv("kplr010666592-2011240104155_slc.csv")
print(dati.columns)
dati.head(10)

plt.figure(figsize=(12,8))
plt.xlabel('Time')
plt.ylabel('electron flux (PDC) [$e^-/s$]')
plt.plot(dati["TIME"], dati["PDCSAP_FLUX"], "o",markersize=1)

plt.figure(figsize=(10,8))
plt.errorbar(dati["TIME"], dati["PDCSAP_FLUX"],yerr= dati["PDCSAP_FLUX_ERR"],color="cornflowerblue" ,fmt=".", label="dati")
plt.xlabel('Time')
plt.legend()
plt.title("Flusso di elettroni")
plt.ylabel('electron flux (PDC) [$e^-/s$]')
plt.savefig("graf_tot.png")
plt.savefig("graf_tot.pdf")

df_stretto=dati.loc[(dati["TIME"]<946.25) & (dati["TIME"]>945.65)]

plt.figure(figsize=(10,8))
plt.errorbar(df_stretto["TIME"], df_stretto["PDCSAP_FLUX"],yerr= df_stretto["PDCSAP_FLUX_ERR"],color="cornflowerblue" ,fmt=".", label="dati")
plt.xlabel('Time')
plt.legend()
plt.title("Flusso di elettroni")
plt.ylabel('electron flux (PDC) [$e^-/s$]')
plt.savefig("graf_parz.png")
plt.savefig("graf_parz.pdf")


# 1. Creazione della figura principale
fig, ax = plt.subplots(figsize=(15,10))

ax.errorbar(dati["TIME"], dati["PDCSAP_FLUX"], yerr=dati["PDCSAP_FLUX_ERR"], color="steelblue", fmt=".", alpha=0.6, label="Dati completi")

# Impostazioni grafico principale
ax.set_xlabel('Time')
ax.set_ylabel('electron flux (PDC) [$e^-/s$]')
ax.set_ylim(1.012e6, 1.027e6)
ax.set_title("Flusso di elettroni", fontsize=15)
ax.legend(loc='upper left')

# 2. Creazione dell'inset (riquadro di zoom)
ins_ax = ax.inset_axes([0.65, 0.68, 0.3, 0.28]) # w.r.t. ax

ins_ax.errorbar(df_stretto["TIME"], df_stretto["PDCSAP_FLUX"], yerr=df_stretto["PDCSAP_FLUX_ERR"], color="orange",fmt=".", label="Zoom")

# 3. Effetto Visivo Zoom (Opzionale ma altamente consigliato)
# Questo comando disegna un rettangolo grigio sul grafico principale nella zona dello zoom
# e traccia delle linee che lo collegano fisicamente al riquadro più piccolo
ax.indicate_inset_zoom(ins_ax, edgecolor="gray", alpha=0.5)

fig.savefig("graf.png")
fig.savefig("graf.pdf")
plt.show()
