# machine_de_turing
Cette machine deTuring a été conçue dans le cadre du cours de Calculabilité du Master TAL - Inalco

Pour exécuter le programme

Commande :

python3 machineTuring.py <NOMFICHIERFONCTION>

ex. :
	python3 machineTuring.py fonction1.txt

Lorsque nous exécutons le script, nous devons insérer les caractères qui composent le ruban, le programme nous demande d'insérer les caractères du ruban.

Obs.: ne pas utiliser les caractères 'i' ou 'f' sur le ruban ! Ces caractères sont utilisés pour la machine pour indiquer le début et la fin du ruban respectivement. Ils sont insérés automatiquement par le script après que nous avons inséré les caractères du ruban.


Fichier de fonction

Pour créer un fichier de fonctions, nous avons les commandes suivantes:

Fonctions de lecture et de déplacement de la tête

l ou L - lire l'état actuel de la machine. À chaque appelle de la commande de lecture, la position de la tête est affichée sur le terminal.

e ou E- écrire un caractère sur le ruban dans la position actuelle de la tête le lecture. Obs: le caractère à être écrire vient immédiatement après le 'e'
ex.:
	e1 - écrit '1'
	e 1 - écrit ' '

d ou D - déplace la tête de lecture une case à droite.
g ou G - déplace la tête de lecture une case à gauche.


Teste logique

! - opérateur négation, indique le contraire de la condition. 
Ex.: 

	pq{!0} e0d 

(pendant que l'état ne soit pas 0, écrire 0 et déplacer la tête vers la droite)


si{<condition>} - teste 'si' - (équivaut le 'if) - exécute un bloc de code si la condition est vraie.
ex.:
	si{0} e1d  (si l'état actuel est zéro, écrit le caractère 1 et déplace la tête à droite)


Boucles

pd{<condition>} - la boucle "pendant que" - (équivaut le 'while') - exécute des blocs de code pendant que la condition de l'état soit vraie. 
ex.:

	pd{!f} e0d

Explication du code : si l'état n'est pas le symbole de fin de ruban, écrit le caractère 0 et déplace la tête de lecture à droite.

jq{<nb_repetion>} - la boucle "jusqu'à" - (équivaut le 'for') - exécute des blocs de code le nombre de fois indiqué par le nombre indiqué para l'utilisateur.
ex. :

	jq{4} d  

Explication du code : il déplace la tête de lecture 4 fois a droite.


Autres commandes

# - le caractère dièse indique la fin du programme

// - ces caractères indiquent un commentaire. Tout ce qui vient après le // est ignoré par la machine. 


Syntaxe

Les commandes peuvent être placés sur une seule ligne ou chaque commande dans une ligne différente.

Ex. :

	de1de0l  

Le code ci-dessus a le même effet que :

	d
	e1
	d
	e0
	l

Dans les boucles pq et jq, et dans le test si, les différents blocs de commandes à être exécuter doivent être sur la même ligne séparés par | 
Ex.:
	jq{10} si{1}e0d | si{0}e1d 

Le code ci-dessous répète 10 fois les testes suivants: si 1, on écrit 0 et déplace la tête à droite, si 0, on écrit 1 et déplace la tête à droite.
Sans le caractère de division « | » , le code suivant ne donnerait pas le même résultat:
Ex. : 
	jq{10} si{1}e0d si{0}e1d 

Le deuxième 'si' mis en évidence n'est exécuté que si le premier 'si' est vrai.

Astuces :

Dans la boucle 'pd' et dans le teste 'si', on n'est pas obligé d'utiliser la commande de lecture 'l' pour évaluer l'état de la machine. Lorsqu'elles sont utilisées, ces commandes lisent automatiquement l'état de la machine.
