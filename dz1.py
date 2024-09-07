#region Randomizacija
def LKG():
    global u
    return (iurng() % 4294967296) /4294967296

def iurng():
    global u
    u = 429493445 * u + 907633385
    return u
def setSeed():
    global u

    while True:
        try:
            print("Unesite seed:")
            u = int(input())
        except:
            print("Pogresan unos!")
        else:
            break

def kockica():

    while True:
        bacanje = LKG()
        if bacanje < 0.16:
            return 1
        elif bacanje < .16*2:
            return 2
        elif bacanje < .16*3:
            return 3
        elif bacanje < .16*4:
            return 4
        elif bacanje < .16*5:
            return 5
        elif bacanje < .16*6:
            return 6

def BacajKockice(br=5,Ispisi = True):
    bacanje = [kockica() for k in range(br)]
    if Ispisi:
        print(bacanje)
    return bacanje
#endregion

def ocistiRetkuMatricu():
    global v,c,r
    v.clear()
    r.clear()
    c.clear()

def upisiUTablu(i, j, vrednost):
    global popunjenaPolja,krajIgre
    global koristiSeMatrica, matrica

    if koristiSeMatrica == False:
        upisiURetkuMatricu(i, j, vrednost)
        if proveriEfikasnost() == False:
            koristiSeMatrica = True
            print("Konvertovalo se u matricu!")
            matrica = konvertuUObicnuMatricu()
            ocistiRetkuMatricu()
            pass
    else:
        if vrednost == 0:
            vrednost = -1
        matrica[i][j] = vrednost
    popunjenaPolja += 1

    if popunjenaPolja >= n*m:
        krajIgre = True


    return True

def ocitajVrednostIzTable(i, j):
    if koristiSeMatrica:
        return matrica[i][j]
    else:
        return ocitajIzRetkeMatrice(i,j)




def upisiURetkuMatricu(i,j,vrednost):
    global v, r, c, m, n

    if vrednost == 0:
        PrecrtajPolje(i,j)
        return False

    if i >= len(r)-1:

        t = r.pop(-1)
        for k in range(i-len(r)): # dodaje se -1 (sve nulte vrednosti u redu) za redove koji su iza reda koji se upisuje
            r.append(-1)

        c.append(j)
        v.append(vrednost)

        r.append(len(c)-1)
        r.append(t)

        r[-1] += 1
        return True

    if r[i] == -1:
        krajIndeks = NadjiKrajnjiIndeks(i)
        krajCIndeks = r[krajIndeks] if krajIndeks != None else len(c)

        r[i] = krajCIndeks
        c.insert(krajCIndeks, j)
        v.insert(krajCIndeks, vrednost)
        pomeriR(i)

        r[-1] += 1
        return True



    pocetniCIndeks = r[i]
    ki = NadjiKrajnjiIndeks(i)
    krajnjiCIndeks = r[ki] if ki != None else len(c)

    for k in range(pocetniCIndeks, krajnjiCIndeks):
        if c[k] >= j:
            c.insert(k,j)
            v.insert(k,vrednost)
            pomeriR(k)
            return True

    c.insert(krajnjiCIndeks,j)
    v.insert(krajnjiCIndeks,vrednost)
    pomeriR(i)

    r[-1] += 1
    return True


def NadjiPocetniIndeks(i):
    for k in range(i, -1, -1):
        if r[k] != -1:
            return k
    return None

def NadjiKrajnjiIndeks(i):
    for k in range(i, len(r)-1):
        if r[k] != -1:
            return k
    return None


def pomeriR(i):
    for k in range(i+1, len(r)-1):
        if r[k] == -1:
            continue
        r[k] += 1
    return True

def konvertuUObicnuMatricu():
    global v,r,c,m,n
    matrica = [[0] * n for k in range(m)]
    for i in range(len(r)-1):
        if r[i] == -1:
            continue
        pocetak = r[i]
        f = 1
        kraj = r[i+f] if i+f < len(r)-1 else len(c)

        while kraj == -1:
            f+=1
            kraj = r[i + f] if i + f < len(r)-1 else len(c)

        for j in range(pocetak, kraj):
            matrica[i][c[j]] = v[j]

    #print("Nenultih elemenata: ",r[-1])

    return matrica

def proveriEfikasnost():
    return (1-len(c)/(m*n)) > .8
def IspisiMeni():
    global krajIgre
    print("#####################################",
          "1. Stvaranje praznog talona za igru",
          "2. Ispis talona",
          "3. Odigravanje jednog poteza",
          "4. Pomoc prijatelja",
          "5. Prekid programa",
          "#####################################",sep="\n")
    opcija = input()
    if opcija == "1":
        stvaranjePraznogTalona()
    elif opcija == "2":
        ispisiTalon()
    elif opcija == "3":
        OdigrajPotez()
    elif opcija == "4":
        PomocPrijatelja()
    elif opcija == "5":
        krajIgre = True

def stvaranjePraznogTalona():
    global sumePoKolonama,koristiSeMatrica,v,r,c

    matrica.clear()

    v = []# v.clear()
    c = []# c.clear()
    r = [0]# r.clear()

    koristiSeMatrica = False
    sumePoKolonama = [0]*6

def ispisiTalon():
    if koristiSeMatrica == False:
        izlaz = konvertuUObicnuMatricu()
    else:
        izlaz = matrica

    global sumePoKolonama
    for i in range(m):
        print(" ".join([str(k) if k != -1 else "X" for k in izlaz[i]]))
        if i == 5:
            print("===================",
                  " ".join([str(k) for k in sumePoKolonama[0:3]]),
                  "===================", sep="\n")

    print("===================",
          " ".join([str(k) for k in sumePoKolonama[3:]]),
          "===================", sep="\n")




    #IspisiPoeneZaSvakuKolonu(matrica)

def IspisiPoeneZaSvakuKolonu(matrica):
    poeni = []

    for j in range(n):
        suma = 0
        for i in range(m):
            suma += matrica[i][j]
        poeni.append(suma)

    print("-----------------------")
    print(f"Na dole: {poeni[0]}",
          f"Na gore: {poeni[1]}",
          f"Rucna: {poeni[2]}",sep="\n")

def OdigrajPotez():
    bacanja = []
    brBacanja = 0
    krajPoteza = False

    bacanja = BacajKockice()
    brBacanja += 1


    print("Da li zelite da popunite kolonu rucna? (y/n):")
    if input() == "y":
        while(True):
            try:
                vrednost = int(input("Unesite red za koji popunjavate (7 - kenta, 8 - ful, 9 - poker, 10 - jamb) : "))
                if popuniRucnu(bacanja,vrednost, brBacanja) == False:
                    raise Exception
            except:
                print("Nevalidan unos!")
            else:
                break
        return True



    if IzborPopunjavanja(bacanja, brBacanja):
        return True

    while brBacanja < 3:
        print("Redni broj kockica koje se ponovo bacaju:")
        ulaz = input().split()
        ponovo = [int(i)-1 for i in ulaz]

        for i in ponovo:
            bacanja[i] = kockica()
        print(bacanja)
        brBacanja += 1

        if IzborPopunjavanja(bacanja, brBacanja):
            return True

def IzborPopunjavanja(bacanja, potez):
    print("Kako zelite da popunite tabelu?")
    print("1. Na dole",
          "2. Na gore",
          "3. Precrtaj polje",sep="\n")

    if potez < 3:
        print("4. Bacaj opet")

    while(True):
        try:
            opcija = input()
            if potez < 3:
                if int(opcija) > 4 and int(opcija) < 1:
                    raise Exception
            else:
                if int(opcija) > 3 and int(opcija) < 1:
                    raise Exception

        except:
            print("Pogresan unos!")
        else:
            break

    if opcija == "1":
        return popuniNaDole(bacanja, potez)
    elif opcija == "2":
        return popuniNaGore(bacanja, potez)
    elif opcija == "3":
        while(True):
            try:
                print("Unesite polje koje zelite da precrtate(0 - na dole, 1 - na gore, 2 - rucna )")
                kolona = input()

                if kolona == "2":
                    print("Unesite red koji popunjavate:")
                    red = input()
                elif kolona == "0":
                    red = poslednjaVrednostNaDole
                elif kolona == "1":
                    red = poslednjaVrednostNaGore
                else:
                    raise Exception

                if PrecrtajPolje(int(red) - 1, int(kolona)) == False:
                    raise Exception
            except:
                print("Pogresan unos!")
            else:
                break
        return True

    return False

def PrecrtajPolje(i,j):
    if ocitajVrednostIzTable(i,j) != 0:
        return False
    upisiUTablu(i,j,-1)
    return True

def popuniRucnu(bacanja,vrednost, potez):
    j = 2
    if ocitajVrednostIzTable(vrednost-1, j) != 0:
        return False

    upisanoUDonjiDeo = True
    rezultat = 0
    if vrednost <= 6:
        rezultat = bacanja.count(vrednost) * vrednost
        upisanoUDonjiDeo = False
    elif vrednost == 7:
        #kenta
        rezultat = izracunajKentu(bacanja,potez)
    elif vrednost == 8:
        #ful
        rezultat = izracunajFul(bacanja)
    elif vrednost == 9:
        #poker
        rezultat = izracunajPoker(bacanja)
    elif vrednost == 10:
        #jamb
        rezultat = izracunajJamb(bacanja)

    upisiUTablu(vrednost-1, j, rezultat)

    if upisanoUDonjiDeo:
        sumePoKolonama[5] += rezultat
    else:
        sumePoKolonama[2] += rezultat

    #print(ispisiTalon())
    #slobodnaPoljaRucna[vrednost-1] = False
    return True

def popuniNaDole(bacanja, potez):
    global poslednjaVrednostNaDole
    global sumePoKolonama

    while ocitajVrednostIzTable(poslednjaVrednostNaDole-1, 0) == -1:
        povecajNaDole()

    if poslednjaVrednostNaDole > 10:
        return False
    upisanoUDonjiDeo = True

    rezultat = 0
    if poslednjaVrednostNaDole <= 6:
        rezultat = bacanja.count(poslednjaVrednostNaDole)*poslednjaVrednostNaDole
        upisanoUDonjiDeo = False
    elif poslednjaVrednostNaDole == 7:
        #kenta
        rezultat = izracunajKentu(bacanja, potez)
    elif poslednjaVrednostNaDole == 8:
        #ful
        rezultat = izracunajFul(bacanja)
    elif poslednjaVrednostNaDole == 9:
        #poker
        rezultat = izracunajPoker(bacanja)
    elif poslednjaVrednostNaDole == 10:
        #jamb
        rezultat = izracunajJamb(bacanja)

    upisiUTablu(poslednjaVrednostNaDole - 1, 0, rezultat)
    povecajNaDole()

    if upisanoUDonjiDeo:
        sumePoKolonama[3] += rezultat
    else:
        sumePoKolonama[0] += rezultat

    return True

def popuniNaGore(bacanja, potez):
    global poslednjaVrednostNaGore

    while ocitajVrednostIzTable(poslednjaVrednostNaGore-1,1) == -1:
        smanjiNaGore()

    if poslednjaVrednostNaGore < 1:
        return False

    upisanoUDonjiDeo = True
    rezultat = 0
    if poslednjaVrednostNaGore == 10:
        #jamb
        rezultat = izracunajJamb(bacanja)
    elif poslednjaVrednostNaGore == 9:
        #poker
        rezultat = izracunajPoker(bacanja)
    elif poslednjaVrednostNaGore == 8:
        #ful
        rezultat = izracunajFul(bacanja)
    elif poslednjaVrednostNaGore == 7:
        #kenta
        rezultat = izracunajKentu(bacanja, potez)
    else:
        rezultat = bacanja.count(poslednjaVrednostNaGore)*poslednjaVrednostNaGore
        upisanoUDonjiDeo = False


    upisiUTablu(poslednjaVrednostNaGore - 1, 1, rezultat)
    smanjiNaGore()

    if upisanoUDonjiDeo:
        sumePoKolonama[4] += rezultat
    else:
        sumePoKolonama[1] += rezultat

    return True

def povecajNaDole():
    global naDoleKraj, poslednjaVrednostNaDole
    poslednjaVrednostNaDole += 1

    if poslednjaVrednostNaDole > 10:
        naDoleKraj = True
    pass


def smanjiNaGore():
    global naGoreKraj, poslednjaVrednostNaGore

    poslednjaVrednostNaGore -= 1

    if poslednjaVrednostNaGore < 0:
        naGoreKraj = True
def ocitajIzRetkeMatrice(i,j):
    global v, r, c, m, n

    if i >= len(r) - 1:
        return 0

    pocetakKolone = r[i]
    br = 1
    krajKolone = r[i+br] if i+1 < len(c) else len(c)
    if pocetakKolone == -1:
        return 0
    while krajKolone == -1 and i+br < len(r)-1:
        br += 1
        krajKolone = r[i+br]
    for k in range(pocetakKolone, krajKolone):
        if c[k] == j:
            return v[k]

    return 0

def mozeKenta(bacanja):
    return bacanja == [2,3,4,5,6] or bacanja == [1,2,3,4,5]
def izracunajKentu(bacanja, potez):
    if mozeKenta(sorted(bacanja)) == False:
        return 0
    kentaBodovi = [66, 56, 46]  # index predstavlja broj bacanja
    return kentaBodovi[potez-1]
def mozeFul(bacanja):
    skup = set(bacanja)
    if len(skup) != 2:
        return False
    k = bacanja.count(bacanja[0])
    return k == 3 or k == 2
def izracunajFul(bacanja):
    if mozeFul(bacanja) == False:
        return 0
    return sum(bacanja) + 30
def mozePoker(bacanja):
    skup = set(bacanja)
    for element in skup:
        if bacanja.count(element) == 4:
            return True
    return False
def izracunajPoker(bacanja):
    if mozePoker(bacanja) == False:
        return 0
    return sum(bacanja)+40
def mozeJamb(bacanja):
    return len(set(bacanja)) == 1
def izracunajJamb(bacanja):
    if mozeJamb(bacanja) == False:
        return 0
    return sum(bacanja)+50





    # izbor kockica koje ponovo baca

def MozeDonjaStrana(bacanja,red):
    if red == 7:
        return mozeKenta(bacanja)
    elif red == 8:
        return mozeFul(bacanja)
    elif red == 9:
        return mozePoker(bacanja)
    elif red == 10:
        return mozeJamb(bacanja)

def IzracunajDonjaStrana(bacanja, red, potez = 0):
    if red == 7:
        return izracunajKentu(bacanja,potez)
    elif red == 8:
        return izracunajFul(bacanja)
    elif red == 9:
        return izracunajPoker(bacanja)
    elif red == 10:
        return izracunajJamb(bacanja)


#region PomocPrijatelja
def PomocPrijatelja():
    global poslednjaVrednostNaDole,poslednjaVrednostNaGore,naDoleKraj, naGoreKraj

    pragVerovatnoce = .3 #.35

    bacanja = BacajKockice()

    potez = 1

    for i in range(7,11):
        if MozeDonjaStrana(bacanja, i):
            popuniRucnu(bacanja, i, potez)
            return True

    for k in bacanja:
        if popuniRucnu(bacanja, k, potez):
            return True

    if naDoleKraj and naGoreKraj:
        for i in range(10):
            if PrecrtajPolje(i, 2):
                break
        return False


    if naDoleKraj:
        OdigrajPotezPP(False, bacanja)
        return True

    if naGoreKraj:
        OdigrajPotezPP(True, bacanja)
        return True



    if poslednjaVrednostNaGore <= 6 and poslednjaVrednostNaDole > 6:
        if IzracunajVerovatnocuDonjaStranaTabele(bacanja,poslednjaVrednostNaDole) > pragVerovatnoce:
            OdigrajPotezPP(True, bacanja)
        else:
            OdigrajPotezPP(False, bacanja)
    elif poslednjaVrednostNaGore <= 6 and poslednjaVrednostNaDole <= 6:

        if bacanja.count(poslednjaVrednostNaDole) >= bacanja.count(poslednjaVrednostNaGore):
            OdigrajPotezPP(True,bacanja)
        else:
            OdigrajPotezPP(False, bacanja)
    elif poslednjaVrednostNaGore > 6 and poslednjaVrednostNaDole > 6:
        if IzracunajVerovatnocuDonjaStranaTabele(bacanja,poslednjaVrednostNaDole) > IzracunajVerovatnocuDonjaStranaTabele(bacanja,poslednjaVrednostNaGore):
            OdigrajPotezPP(True,bacanja)
        else:
            OdigrajPotezPP(False,bacanja)
    elif poslednjaVrednostNaGore >6 and poslednjaVrednostNaDole <=6:
        if IzracunajVerovatnocuDonjaStranaTabele(bacanja, poslednjaVrednostNaGore) > pragVerovatnoce:
            OdigrajPotezPP(False,bacanja)
        else:
            OdigrajPotezPP(True, bacanja)
    #print(poslednjaVrednostNaGore,poslednjaVrednostNaDole)

def BrojKockicaKojeSePonovoBacaju(bacanje,red):
    izbaceneKockice = []
    ostaleKockice = []

    print("Izabrana", red)
    if red == 7:
        kenta = [1, 2, 3, 4, 5]

        for i in kenta:
            if i not in bacanje:
                izbaceneKockice.append(i)
            else:
                ostaleKockice.append(i)

        izbaceneKockice2 = []
        ostaleKockice2 = []

        kenta = [2, 3, 4, 5, 6]
        for i in kenta:
            if i not in bacanje:
                izbaceneKockice2.append(i)
            else:
                ostaleKockice2.append(i)
        if len(izbaceneKockice2) > len(izbaceneKockice):
            return (izbaceneKockice, ostaleKockice)
        else:
            return (izbaceneKockice2,ostaleKockice2)
    elif red == 8:

        broj, maks = NajvisePonavljanja(bacanje)
        brKockicaKojeSePonovoBacaju = 3 - maks
        ostaleKockice += [broj]*maks

        for k in range(maks):
            bacanje.remove(broj)

        broj, maks = NajvisePonavljanja(bacanje)
        brKockicaKojeSePonovoBacaju += 2 - maks
        ostaleKockice += [broj]*maks
        izbaceneKockice = OduzmiDveListe(bacanje,ostaleKockice)
        pass


    elif red == 9:
        broj, maks = NajvisePonavljanja(bacanje)
        ostaleKockice = [broj]*maks
        izbaceneKockice = OduzmiDveListe(bacanje,ostaleKockice)

    elif red == 10:
        broj, maks = NajvisePonavljanja(bacanje)
        ostaleKockice = [broj]*maks
        izbaceneKockice = OduzmiDveListe(bacanje,ostaleKockice)


    return (izbaceneKockice,ostaleKockice)

def OduzmiDveListe(x,y):
    return [k for k in x if k not in y]
def OdigrajPotezPP(naDole, bacanje):
    global poslednjaVrednostNaDole, poslednjaVrednostNaGore

    if naDole:
        if 1 <= poslednjaVrednostNaDole <= 6:
            for i in range(1, 4):
                if poslednjaVrednostNaDole in bacanje:
                    popuniNaDole(bacanje, i)
                    return True
                if i == 3:
                    break
                bacanje = BacajKockice()

            PrecrtajPolje(poslednjaVrednostNaDole - 1, 0)
            povecajNaDole()
            return False


        for i in range(1,4):
            if MozeDonjaStrana(bacanje, poslednjaVrednostNaDole):
                popuniNaDole(bacanje, i)
                return True
            if i == 3:
                break
            izbacene, ostale = BrojKockicaKojeSePonovoBacaju(bacanje, poslednjaVrednostNaDole)
            bacanje = BacajKockice(len(izbacene),False) + ostale
            print("Bacanje",bacanje)


        PrecrtajPolje(poslednjaVrednostNaDole-1,0)
        povecajNaDole()

    else:
        if 1 <= poslednjaVrednostNaGore <= 6:
            for i in range(1, 4):
                if poslednjaVrednostNaGore in bacanje:
                    popuniNaGore(bacanje, i)
                    return True
                if i == 3:
                    break
                bacanje = BacajKockice()

            PrecrtajPolje(poslednjaVrednostNaGore - 1, 1)
            smanjiNaGore()
            return False

        for i in range(1, 4):
            if MozeDonjaStrana(bacanje, poslednjaVrednostNaGore):
                popuniNaGore(bacanje, i)
                return True
            if i == 3:
                break
            izbacene, ostale = BrojKockicaKojeSePonovoBacaju(bacanje, poslednjaVrednostNaGore)
            bacanje = BacajKockice(len(izbacene), False) + ostale
            print("Bacanje", bacanje)

        PrecrtajPolje(poslednjaVrednostNaGore - 1, 1)
        smanjiNaGore()

def IzracunajVerovatnocuDonjaStranaTabele(bacanja,red):
    bacanja2 = bacanja.copy()
    if red == 7:
        return IzracunajVerovatnocuKenta(bacanja2)
    elif red == 8:
        return IzracunajVerovatnocuFul(bacanja2)
    elif red == 9:
        return IzracunajVerovatnocuPoker(bacanja2)
    elif red == 10:
        return IzracunajVerovatnocuJamb(bacanja2)

def IzracunajVerovatnocuPoker(bacanja):
     #2 2 2 2 X
    #1 2 2 3 3
    if mozePoker(bacanja):
        return 1.0

    broj,maks = NajvisePonavljanja(bacanja)

    kombinacija = [broj]*(4-maks)+["X"]
    return IzracunajVerovatnocu(kombinacija)
def NajvisePonavljanja(bacanja):
    maks = 0
    broj = 0
    for i in set(bacanja):
        br = bacanja.count(i)
        if br > maks:
            broj = i
            maks = br
    return (broj, maks)
def IzracunajVerovatnocuJamb(bacanja):
    #2 2 2 2 2
    #1 2 2 3 4
    if mozeJamb(bacanja):
        return 1.0

    broj,maks = NajvisePonavljanja(bacanja)

    kombinacija = [broj]*(5-maks)
    return IzracunajVerovatnocu(kombinacija)
def IzracunajVerovatnocuFul(bacanja):
    if mozeFul(bacanja):
        return 1.0
    # 2 2 3 3 3
    # 3 2 1 5 6

    broj, maks = NajvisePonavljanja(bacanja)
    kombinacija = [broj]*(3-maks)

    for i in range(maks):
        bacanja.remove(broj)
    broj, maks = NajvisePonavljanja(bacanja)
    kombinacija += [broj]*(2-maks)

    return IzracunajVerovatnocu(kombinacija)
def IzracunajVerovatnocuKenta(bacanja):
    if mozeKenta(bacanja):
        return 1.0

    #1 2 3 4 5  V 2 3 4 5 6
    #2 2 4 5 1
    kombinacija = []
    kenta = [1,2,3,4,5]
    #kenta2 = [2,3,4,5,6]
    for i in kenta:
        if i not in bacanja:
            kombinacija.append(i)

    verovatnoca = IzracunajVerovatnocu(kombinacija)

    kombinacija = []
    kenta = [2,3,4,5,6]
    for i in kenta:
        if i not in bacanja:
            kombinacija.append(i)

    return max(verovatnoca,IzracunajVerovatnocu(kombinacija))

def IzracunajVerovatnocu(kombinacija,brojBacanja = 550):
    # 2 2 X
    br = 0
    brKockica = len(kombinacija)
    #ukupnoKombinacija = 6**brKockica
    for i in range(brojBacanja):
        bacanje = BacajKockice(brKockica,False)
        if ProveriPrviPut(bacanje, kombinacija):
            br += 1

    #print(kombinacija,br/brojBacanja)
    return br/brojBacanja
def ProveriPrviPut(bacanje, kombinacija):
    drugaKombinacija = []
    brNadjenih = 0
    # 2 6 5 5 =
    # 2 5 5 5  =>2 5
    #
    brKockica = len(bacanje)
    for i in set(kombinacija):
        if i == "X":
            continue

        istihKombinacije =kombinacija.count(i)
        istihBacanje = bacanje.count(i)
        brRazlike = istihKombinacije - istihBacanje
        brRazlike = brRazlike if brRazlike > 0 else 0 # ako je nula svi su nadjeni
        drugaKombinacija.extend([i]*brRazlike)

        if istihBacanje > istihKombinacije:
            brKockica -= istihKombinacije
        else:
            brKockica -= istihBacanje

    if len(drugaKombinacija) == 0:
        return True
    else:
        return ProveriDrugiPut(drugaKombinacija,brKockica)

def ProveriDrugiPut(kombinacija,brKockica):
    bacanje = [kockica() for k in range(brKockica)]
    for i in set(kombinacija):
        if bacanje.count(i) < kombinacija.count(i):
            return False
    return True


#endregion



#Retka matrica - preko 80% nultih elemenata

naDoleKraj = False
naGoreKraj = False

#slobodnaPoljaRucna = [True]*10

popunjenaPolja = 0

matrica = []
koristiSeMatrica = False


krajIgre = False

sumePoKolonama = [0, 0, 0, 0, 0, 0]

setSeed()


m = 10
n = 3

poslednjaVrednostNaDole = 1
poslednjaVrednostNaGore = 10

ukupnoElemenata = m*n
r = [0]
v = []
c = []

stvaranjePraznogTalona()

while krajIgre == False:
    IspisiMeni()

ispisiTalon()
print("Igra je zavrsena!")

