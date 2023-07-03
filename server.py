import random

lettres = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

pendu = [
    """
       
       
       
       
       
       
       
    ==============
    """,
    """
       
       |
       |
       |
       |
       |
       |
    ==============
    """,
    """
       +-------+
       |
       |
       |
       |
       |
       |
    ==============
    """,
    """
       +-------+
       |       |
       |       O
       |
       |
       |
       |
    ==============
    """
        ,
    """
       +-------+
       |       |
       |       O
       |       |
       |
       |
       |
    ==============
    """,
    """
       +-------+
       |       |
       |       O
       |     --|
       |
       |
       |
    ==============
    """,
    """
       +-------+
       |       |
       |       O
       |     --|--
       |
       |
       |
    ==============
    """,
    """
       +-------+
       |       |
       |       O
       |     --|--
       |      |
       |     /
       |
    ==============
    """,
    """
       +-------+
       |       |
       |       O
       |     --|--
       |      | |
       |     /  /
       |
    ==============
    """
    ]

def liste_mots(L):
    f = []
    for i in L:
        f.append(i[0])
    return f

with open("mots.csv","r",encoding="utf8") as f:
    table_mots = []
    ligne = f.readline()
    motVerifLong = ""  
    while ligne != "":
        motVerifLong = ligne.replace("\n","")
        table_mots.append([motVerifLong])
        ligne = f.readline()

table_mots = liste_mots(table_mots)

# Jeu :

# 336531 -> 336437 mots

essais = 0
lettresTrouvees = " "
lettresErreurs = ""
motAffiche = ""
victoire = False
choixUser = ""

motchoisi = random.choice(table_mots)

def robot(liste, viewWord, foire, reussi):
    newListeBot = []
    etude = ""
    indicesDicWnown = {i:"-" for i in range(len(viewWord))}
    for i in liste:
        if len(i) == len(viewWord):
            newListeBot.append(i)
    
    for i in range(len(viewWord)):
        if viewWord[i] != "-":
            indicesDicWnown[i] = viewWord[i]

    finalListBot = []

    for motPotentiel in newListeBot:
        scoreforWord = 0
        scoreforWordMax = 0
        erreurDeLettre = False
        for indice,valeur in indicesDicWnown.items():
            if valeur != "-":
                scoreforWordMax += 1 
                if motPotentiel[indice] == valeur:
                    scoreforWord +=1
        if scoreforWord == scoreforWordMax:
            for lettreFoiree in foire:
                if lettreFoiree in motPotentiel:
                    erreurDeLettre = True

            if not(erreurDeLettre):
                finalListBot.append(motPotentiel)

    newListeBot = []

    if viewWord == len(viewWord)*"-":
        return finalListBot

    for motPotentiel in finalListBot:
        for caractAffiche in viewWord:
            for caractPotentiel in motPotentiel:
                if not(caractAffiche == "-" and caractPotentiel in reussi):
                    if not(motPotentiel in newListeBot):
                        newListeBot.append(motPotentiel)


    return newListeBot

def essai():
    global essais,lettresTrouvees,lettresErreurs,motAffiche,choixUser

    motAffiche = ""
    choixUser = ""

    for i in motchoisi:
        if i in lettresTrouvees:
            motAffiche += i
        else:
            motAffiche += "-"
    if motAffiche == motchoisi:
        return True

    #print(motchoisi)
    print(robot(table_mots,motAffiche,lettresErreurs,lettresTrouvees))
    print(pendu[essais])
    print(motAffiche)
    if lettresErreurs != "":
        print("Erreurs : " + lettresErreurs)


    while not(choixUser in lettres) or not(len(choixUser) == 1) or choixUser in lettresTrouvees or choixUser in lettresErreurs:
        choixUser = input("Entrez une lettre : ")
    print(20*"*")

    if choixUser in motchoisi:
        lettresTrouvees += choixUser
    else:
        lettresErreurs += choixUser
        essais += 1
        return False


while essais < 8 and not(victoire):
    victoire = essai()

if victoire == True:
    print("Félicitations ! Tu a gagné !")
    print("Le mot était bien " + motchoisi)
else:
    print("Tu a perdu...")
    print("Le mot était : " + motchoisi)