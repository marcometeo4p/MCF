num=input("inserere il numero di valori interi che si immetteranno")
valori=[]
for i in range(int(num)):
    n2=input(f"immetere il numero {i+1} di {num}")
    if n2.isdigit():
        valori.append(int(n2))
    elif n2[0]=="-" and n2[1:].isdigit():
        print("numero negativo")
        valori.append(-int(n2[1:]))
    else:
        print("il valore inserito non è un numero intero")

for n in valori:
    print("il numero {:10d} in binario è {}; in ottale è {}; in esadecimale è {}".format(n,bin(n),oct(n),hex(n)))

val=[valori[0],valori[1]]
p=val[0]|val[1]
print("(n_1|n_2)={} in binario è {:10b}; in ottale è {:6o}; in esadecimale è {:6x}".format(p,p,p,p))
p=val[0]&val[1]
print("(n_1&n_2)={} in binario è {:10b}; in ottale è {:6o}; in esadecimale è {:6x}".format(p,p,p,p))