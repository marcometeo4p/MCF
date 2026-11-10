import sposta
import matplotlib.pyplot as plt
import numpy as np

list_s=[1,0.5,0.1,2,2.1]
N=10000
rd_w=[]
fig, ax = plt.subplots(1,2,figsize=(10, 6))
for i in range(len(list_s)):
    c=sposta.spost(N,list_s[i])
    rd_w.extend(c)
    ax[0].scatter(c[0], c[1], s=1, alpha=0.5, label=f's={list_s[i]}')
    ax[1].plot(np.arange(1, N+2), c[0]**2 + c[1]**2, alpha=0.5, linewidth=1,label=f's={list_s[i]}')
plt.title('Spostamenti casuali in 2D')
ax[0].set_title('Traiettorie Random Walk 2D')
ax[0].set_xlabel('X')
ax[0].set_ylabel('Y')
ax[1].set_xlabel('Passo')
ax[1].set_ylabel('Distanza dal punto di partenza')
ax[1].set_title('Distanza quadratica dall\'origine')
plt.legend()
plt.savefig('spostamenti_casuali.png')
plt.show()