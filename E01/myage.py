from datetime import datetime,timedelta 
def stampa(oggi):
    print("\n Anno: {}\n Mese: {}\n Giorno: {}".format(oggi.year,oggi.month,oggi.day))
oggi=datetime.now()
print("oggi è:")
stampa(oggi)
g=input("inserire giorno di nascita:")
m=input("inserire mese di nascita:")
y=input("inserire anno di nascita:")
h=input("inserire ora del giorno di nascita:")
i=input("inserire minuto di nascita:")
nasc=datetime(int(y),int(m),int(g),int(h),int(i))
print("sei nato il:")
stampa(nasc)
print("\n alle {}:{}\n".format(nasc.hour,nasc.minute))
diff_mesi=oggi.month-nasc.month
diff_anni=oggi.year - nasc.year +diff_mesi//12 #toglie compleanno non raggiunto
diff_giorni=oggi.day-nasc.day
eta =oggi-nasc
print("la tua età è: {} anni e {} mesi".format(diff_anni, diff_mesi % 12))
eta=oggi-nasc
print('ovvero {} giorni {} ore {} minuti {}.{} secondi'.format(eta.days, eta.seconds // 3600, (eta.seconds % 3600) // 60, eta.seconds % 60,eta.microseconds))
print("o {} giorni".format(eta.total_seconds()//(3600*24)))
print("o {} secondi".format(eta.total_seconds()))

print("\n =======================FORMATTAZIONE========================\n")
print("oggi è: {:02d}/{:02d}/{:04d} {:02d}:{:02d}".format(oggi.day,oggi.month,oggi.year,oggi.hour,oggi.minute))
print("sei nato il: {:02d}/{:02d}/{:04d} {:02d}:{:02d}".format(nasc.day,nasc.month,nasc.year,nasc.hour,nasc.minute))
print("\nla tua età è: {:<4f} anni ".format(eta.total_seconds()/(3600*24*365.25)))
print("\nla tua età è: {:.4f} giorni".format(eta.total_seconds()/(3600*24)))
print("la tua età è: {:.4f} secondi".format(eta.total_seconds()))