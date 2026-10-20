n=input("inserire numero naturale")
#converto in int
num = int(n)
i=somma=0
while i< num+1:
	somma=somma + i
	i=i+1
print("la somma è:{:10}".format(somma))
