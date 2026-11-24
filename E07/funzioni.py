import pandas as pd
import matplotlib.pyplot as plt
def der_centrale(dati,step:int): 
  df_der = pd.DataFrame({
                        'time': [],
                        'der_1': [],
                        'der_2': []})
  df_der['time']=[]
  df=dati
  for l in range(1, int(len(dati['time']) / step) - 1):
      i = l * step
      d=int(step/2)
      df_der.loc[l, 'time'] = df['time'][i]
      df_der.loc[l, 'der_1'] = (df['signal1'][i + d] - df['signal1'][i - d]) / (df['time'][i + d] - df['time'][i - d])
      df_der.loc[l, 'der_2'] = (df['signal2'][i + d] - df['signal2'][i - d]) / (df['time'][i + d] - df['time'][i - d])

  plt.figure(figsize=(15, 10))
  plt.plot(df_der['time'], df_der['der_1'], label='canale 1')
  plt.plot(df_der['time'], df_der['der_2'], label='canale 2')
  plt.xlabel('tempo [s]')
  plt.ylabel('derivata segnale [V/s]')
  plt.title(f"derivate oscilloscopio n={step}", fontsize=20)
  plt.legend()
  plt.savefig(f"ocsilloscopio_n{step}.png")
  plt.show()
  return df_der