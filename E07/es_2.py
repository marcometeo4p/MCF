import pandas as pd
import matplotlib.pyplot as plt
import funzioni
df=pd.read_csv("oscilloscope.csv")
df
plt.figure(figsize=(15,10))
plt.plot(df['time'], df['signal1'], label='canale 1')
plt.plot(df['time'], df['signal2'], label='canale 2')
plt.ylabel('ampiezza del segnale [V]')
plt.title("Oscilloscopio", fontsize=20)
plt.legend()
plt.savefig("ocsilloscopio.png")
plt.show()

steps=[5,25,50,100,200]
data=[]
for s in steps:
    la=funzioni.der_centrale(df,s)
    data.append(la)
dati_min = data[3]  # corrisponde a step = 100
der1 = dati_min['der_1'].reset_index(drop=True)
tempi_der = dati_min['time'].reset_index(drop=True)

mins_idx = []
for i in range(1, len(der1) - 1):
    # Attraversamento dello zero da negativo a positivo -> minimo locale del segnale
    if der1.iloc[i - 1] < 0 and der1.iloc[i + 1] > 0:
        mins_idx.append(i)

t_minimi = tempi_der.iloc[mins_idx]
idx_df = df['time'].searchsorted(t_minimi).clip(0, len(df) - 1)

fig, ax1 = plt.subplots(figsize=(15, 10))

# Asse y sinistro: derivata [V/s]
line1, = ax1.plot(tempi_der, der1, color='tab:blue', label='derivata canale 1')
ax1.axhline(0, color='gray', linestyle='--', linewidth=1)
ax1.set_xlabel('tempo [s]')
ax1.set_ylabel('derivata segnale [V/s]', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Asse y destro (secondario): minimi di signal1 [V] tramite scatter
ax2 = ax1.twinx()
scatter2 = ax2.scatter(df['time'].iloc[idx_df], df['signal1'].iloc[idx_df],
            marker="*", color='red', s=150, label='minimi segnale')
ax2.set_ylabel('ampiezza segnale [V]', color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.title("Derivata oscilloscopio e minimi segnale", fontsize=20)

# Legenda combinata di entrambi gli assi
handles = [line1, scatter2]
labels = [h.get_label() for h in handles]
ax1.legend(handles, labels, loc='best')

plt.tight_layout()
plt.savefig('min1.png')
plt.show()

der1 = dati_min['der_2'].reset_index(drop=True)
tempi_der = dati_min['time'].reset_index(drop=True)

mins_idx = []
for i in range(1, len(der1) - 1):
    # Attraversamento dello zero da negativo a positivo -> minimo locale del segnale
    if der1.iloc[i - 1] < 0 and der1.iloc[i + 1] > 0:
        mins_idx.append(i)

t_minimi = tempi_der.iloc[mins_idx]
idx_df = df['time'].searchsorted(t_minimi).clip(0, len(df) - 1)

fig, ax1 = plt.subplots(figsize=(15, 10))

# Asse y sinistro: derivata [V/s]
line1, = ax1.plot(tempi_der, der1, color='tab:blue', label='derivata canale 2')
ax1.axhline(0, color='gray', linestyle='--', linewidth=1)
ax1.set_xlabel('tempo [s]')
ax1.set_ylabel('derivata segnale [V/s]', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')

# Asse y destro (secondario): minimi di signal1 [V] tramite scatter
ax2 = ax1.twinx()
scatter2 = ax2.scatter(df['time'].iloc[idx_df], df['signal2'].iloc[idx_df],
            marker="*", color='red', s=150, label='minimi segnale')
ax2.set_ylabel('ampiezza segnale [V]', color='red')
ax2.tick_params(axis='y', labelcolor='red')

plt.title("Derivata oscilloscopio e minimi segnale ch2", fontsize=20)

# Legenda combinata di entrambi gli assi
handles = [line1, scatter2]
labels = [h.get_label() for h in handles]
ax1.legend(handles, labels, loc='best')

plt.tight_layout()
plt.savefig('min2.png')
plt.show()