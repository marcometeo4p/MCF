sett = ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica']
id_pr=3
id=0
ott,gg=[],[]
for i in range(31):
    ott.append(sett[(id_pr+i)%7])
    gg.append(i+1)
    #id_pr = (id_pr + 1) % 7

diz_ott=dict(zip(gg, ott))

for (g,s) in diz_ott.items():
    print("il giorno {} è {}".format(g,s))