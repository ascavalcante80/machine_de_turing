__author__ = 'alexandre s. cavalcante'

# todo importante IMPLEMENTAR A LEITURA DO ESTADO PELOS LOOPS!!!! DESTA FORMA NAO PRECISAMOS RELER O ESTADO!!!

import re, sys

nomFichier = sys.argv[1]

try:
    fonction = open(nomFichier, 'r')
except:
    print("Problem lors de l'ouverture du fichier")
    exit(0)    

# variable pour global pour controler la position da la tete de lecture
positionTete = 0

# variable pour global stocker l'etat lu par la machine
etat = ''

""" La fonction interpreterEntree() traite les commandes lues du fichier programme.
    Elle recoit une string comme argument et réalise plusieurs testes afin d'executer les commande contenues dans la string.
"""
def interpreterEntree(line, compteLigne):

    global ruban

    # suprimer retour `a la ligne et metter les lettres en minuscule
    line = line.strip().lower()

    # verifier quelle commande la ligne contient
    while(len(line) > 0):

        # cette variable sert à controler la syntaxe du code.
        syntaxeOk = False

        # ce teste prend en compte les spaces
        if (line.startswith(" ")):
            syntaxeOk = True

        # verifier si la string est un commentaire
        if(line.startswith('//')):
            return

        if (line.startswith('l')):
            fonctionLire(compteLigne)
            syntaxeOk = True

        if (line.startswith('e')):
            fonctionEcrire(line, compteLigne)
            line = line[1:]
            syntaxeOk = True

        if(line.startswith('g') or line.startswith('d')):
            deplaceTete(line)
            syntaxeOk = True

        if(line.startswith('si')):
            testeSi(line, compteLigne)
            return

        # `jq` abregee de jusqu`a
        if(line.startswith('jq')):
            boucleJusquA(line, compteLigne)
            return

        if(line.startswith('pd')):
            bouclePendant(line, compteLigne)
            return

        if(line == '#'):

            print ('Position Final - ' + ''.join(ruban))

            bougeFleche = ' ' * positionTete
            print ('                 ' + bougeFleche +'⇡')

            print('fin du programme')
            exit(0)

        if not (syntaxeOk):
            print('Erro ligne' + str(compteLigne) + ' : Syntaxe incorrecte')
            exit(0)
        # reduction des caracteres inutiles ou deja lus
        line = line[1:]

""" Cette fonction lit l`etat de la position actuel de la tete de lecture.
 Chaque fois que cette fonction est appellee, elle affiche le ruban avec la position de la tete sur le terminal.
"""
def fonctionLire(compteLigne):

    global positionTete, ruban, etat

    # verifier si la position de la tete ne depasse pas la taille du ruban
    if (positionTete < len(ruban)):

        # actualiser la valeur da la variable globale etat
        etat = ruban[positionTete]

        print ('lctr - ' + ''.join(ruban))

        bougeFleche = ' ' * positionTete
        print ('       ' + bougeFleche +'⇡')

    else:
        print ('Erro ligne '+ str(compteLigne) +' : position de la tête de lecture dépasse la taille du ruban.')
        exit(0)


"""cette fonction implemente la fonction `ecire`. Elle contient 2 parties obligatoires:
 la commande `e` suivi du caractere a ecrire sur le ruban. Obs. le caracte
"""
def fonctionEcrire(args, compteLigne):

    global positionTete, ruban, etat

    # verifier si le nombre d'argument sur la ligne est correct
    if (len(args) == 1):
        print("Erro ligne "+str(compteLigne) +" : Nombre d`arguments d`ecriture incorrect." )
        exit(0)

    # verifier si la position de la tete ne depasse pas la fin du ruban
    if (positionTete < len(ruban)):

        if ruban[positionTete] == 'i':
            ruban[positionTete] = args[1]
            ruban.insert(0, 'i')
        else:
            ruban[positionTete] = args[1]

        # afficher ruban ave la flèche de position
        print('ecrt - ' + ''.join(ruban))
        # calcule le nb d'espace à rajouter pour deplacer la flèche
        bougeFleche = ' ' * positionTete
        print ('       ' + bougeFleche +'⇡')
    else:
        print ('Erro ligne ' + str(compteLigne) +' : position de la tête de lecture dépasse la taille du ruban.')
        exit(0)


""" cette fonction deplace la tete de lecture.
    Pour eviter le depassement de la tete dans de position plus grandes ou plus petites que la taille du ruban,
    elle verifie la position avant d`attribuer la valeur `a la variable"""
def deplaceTete(line):

    global positionTete, etat

    if (line.startswith('g')):
        positionTete -= 1

        # verifier position de la tete pour eviter une position negative
        if(positionTete < 0):
            positionTete = 0

    elif (line.startswith('d')):
        positionTete += 1

        # verifier position de la tete pour eviter qu`elle depasse le limite du ruban
        if(positionTete > len(ruban) - 1):
            positionTete = len(ruban) - 1


"""cette fonction implemente le teste `si`. chaque teste `si` doit contenir 2 parties obligatoires:
 le condition teste, entourre par {}, et les commandes `a executer si le teste est vrai. Les differentes commandes doivent etre separees par le caractere '|'
"""
def testeSi(line, compteLigne):

    # lire l'etat de la machine
    fonctionLire(compteLigne)

    global etat

    teste = line[2:]

    # verifier si la commande est bien formée
    if not (teste.startswith('{')):
        print("Erro ligne " + str(compteLigne) + " : syntaxe incorrecte. Il manque le '{'")
        exit(0)

    if not ('}' in teste):
        print("Erro " + str(compteLigne) + " : syntaxe incorrecte. Il manque le '}'")
        exit(0)

    # regex pour obtenir la condition `a tester
    regexCondition = re.compile('^si\{(.+?)\}.+$')

    # regex pour obtenir le bloc de code `a executer si la condition est vraie
    regexBlocVrai = re.compile('^si\{\w+\}(.+)$')

    # analiser le bloc d`instructions
    try:

        # exectuer les regex
        blocCondition = regexCondition.match(line).group(1)
        blocVrai = regexBlocVrai.match(line).group(1)

        # verifier si la condition condition l`operateur negation
        if (blocCondition.startswith('!')):

            if (blocCondition != etat):

                # verifier le blocVrai contient plusieurs testes
                if '|' in blocVrai:
                    for item in blocVrai.split('|'):
                        interpreterEntree(item, compteLigne)
                else:
                    interpreterEntree(blocVrai, compteLigne)
        else:
            # bloc `a exectuer si la condition ne contient pas l`operateur negatif
            if (blocCondition == etat):

                 # verifier le blocVrai contient plusieurs testes
                if '|' in blocVrai:
                    for item in blocVrai.split('|'):
                        interpreterEntree(item, compteLigne)
                else:
                    interpreterEntree(blocVrai, compteLigne)
    except:
        print('Erro ligne '+ str(compteLigne) +' : Syntaxe incorrecte')
        exit(0)


"""cette fonction implemente la bloucle `jq` (jusqu`a). chaque bloucle `jq` doit contenir 2 parties obligatoires:
 le nombre d`interactions indique par un nombre entier, entourre par {}, et les commandes `a executer si le teste est vrai. Les differentes commandes doivent etre separees par le caractere '|'
"""
def boucleJusquA(line, compteLigne):

    teste = line[2:]

    # verifier syntaxe
    if not (teste.startswith('{')):
        print("Erro ligne " + str(compteLigne) + " : syntaxe incorrecte. Il manque le '{'")
        exit(0)

    if not ('}' in teste):
        print("Erro ligne " + str(compteLigne) + " : syntaxe incorrecte. Il manque le '}'")
        exit(0)

    try:
        nbRepetions = int(teste[1].split('}')[0])
    except:
        print("Erro ligne " + str(compteLigne) + " : le nombre de iterations doit etrê indiqué par un nombre entier '" + teste[1].split('}')[0] + "' n`est pas un nombre entier" )
        exit(0)

    try:
        regexBloc = re.compile('jq{.+?}(.+)')

        blocRepetion = regexBloc.match(line).group(1)
    except:
        print("Erro ligne " + str(compteLigne) + " : de Syntaxe")
        exit(0)

    if isinstance(nbRepetions, int):

        compteur = 0
        while(compteur < nbRepetions):

            if('|' in blocRepetion):

                for item in blocRepetion.split('|'):
                    interpreterEntree(item, compteLigne)
            else:
                interpreterEntree(blocRepetion, compteLigne)
            compteur += 1
    else:
        print("Erro ligne " + str(compteLigne) + " : Le nombre de répetions doit être un entier.")
        exit(0)

"""cette fonction implemente la boucle `pd`(pendant que). chaque boucle `pd` doit contenir 2 parties obligatoires:
 le condition teste, entourre par {}, et les commandes `a executer si le teste est vrai. Les differentes commandes doivent etre separees par le caractere '|'
"""
def bouclePendant(line, compteLigne):
                
    global etat
    teste = line[2:]

    # verifier syntax
    if not (teste.startswith('{')):
        print("Erro ligne " + str(compteLigne) + " : syntaxe incorrecte. Il manque le '{'")
        exit(0)

    if not ('}' in teste):
        print("Erro ligne " + str(compteLigne) + " : syntaxe incorrecte. Il manque le '}'")
        exit(0)

    try:

        # regex pour obtenir la condtion
        regexCondition = re.compile('^\{(.+?)\}.+$')
        condition = regexCondition.match(teste).group(1)

        # regex pour obtenir le bloc vraie
        regexBlocvrai = re.compile('\{.+?\}(.+)$')
        blocVrai = regexBlocvrai.match(teste).group(1)

    except:
        print('Erro ligne ' + str(compteLigne) + ' : Syntaxe incorrecte')
        exit(0)


    # verifier la condition utilise l'operateur negation
    if (condition.startswith('!')):

        # le code condition[1:] nous permet d'obtenir la valeur de condition sans l'operateur !
        while(etat != condition[1:]):

            # lire l'etat de la machine
            fonctionLire(compteLigne)

            # verifier si le blocVrai contient plusieurs commandes
            if '|' in blocVrai:
                for item in blocVrai.split('|'):
                    interpreterEntree(item, compteLigne)
            else:
                interpreterEntree(blocVrai, compteLigne)
    else:

        # bloc à executer si la condition ne contient pas l'operateur !
        while(etat == condition):

            # lire l'etat de la machine
            fonctionLire(compteLigne)

            # verifier si le blocVrai contient plusieurs commandes
            if '|' in blocVrai:
                for item in blocVrai.split('|'):
                    interpreterEntree(item, compteLigne)
            else:
                interpreterEntree(blocVrai, compteLigne)


entreUtilisateur = input("Tapez les caracteres du ruban: \n")

ruban = list("i" + entreUtilisateur + "f")

compteLigne = 1

for line in fonction:

    interpreterEntree(line, compteLigne)
    compteLigne +=1
