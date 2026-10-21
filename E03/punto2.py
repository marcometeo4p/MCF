n=input("inserire numero intero")
sh=input("inserire numero di bin da shiftare")

n=int(n)
sh=int(sh)
print("il numero inserito è {:10d} in binario è {:10b}; in ottale è {:8o}; in esadecimale è {:6x}".format(n,n,n,n))
print("il numero di shift è {:10d} in binario è {:10b}; in ottale è {:8o}; in esadecimale è {:6x}".format(sh,sh,sh,sh))

s1=(n >> sh)
s2=(n << sh)

print("il numero shiftato >> è {:10d} in binario è {:10b}; in ottale è {:8o}; in esadecimale è {:6x}".format(s1,s1,s1,s1))
print("il numero shiftato << è {:10d} in binario è {:10b}; in ottale è {:8o}; in esadecimale è {:6x}".format(s2,s2,s2,s2))