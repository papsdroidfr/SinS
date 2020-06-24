# SinS
Jeux de mémoire visuelle et auditive à base d'une PYBStick26,.

Il faut retrouver les clés de 10 coffres à trésors cachés dans un immense labyrinthe.

Dans chaque pièce où vous entrez, il y a 4 sorties de 4 couleurs distinctes. Vous avez un guide qui ouvre le chemin et vous montre les  3 prochaines portes à ouvrir pour trouver une première clé. Si vous réussissez, votre guide vous montre alors les 3 portes suivantes à ouvrir y compris les 3 premières déjà empruntées, et ainsi de suite... Le jeux se termine quand vous avez raporté les 10 clés, ou bien quand vous vous trompez et êtes perdu dans le labyrinthe.

## matériel nécessaire
* 1 PYBStick26
* 4 leds 5mm (Verte, Bleue, Jaune, Rouge)
* 4 résistances 220 ohms (pour les leds)
* 1 transistor npn (TO92)
* 1 résistance 1k ohms (pour le transistor)
* 1 petit buzzer passif
* 4 petits boutons poussoir 6mm
* 1 écran LCD 1602 avec backpack I2C

## prototypage sur breadboard

![prototype breadbaord](_docs/SinS_bb.png)

## scripts micropython à installer sur la PYBStick
Dans le répertoire PYBFLASH qui s'affiche à l'ordinateur lors du branchement de la PYBStick26 sur un port USB, déposez tous les fichiers Micropython ci-dessous:
* buttons.py : gestion du rack de boutons poussoirs
* buzzer.py  : gestion du buzzer
* lcd.py     : gestion du LCD
* lcd2ic.py  : conçu par [MC Hobby](https://github.com/mchobby/pyboard-driver/tree/master/PYBStick): gestion du LCD via I2C de la PYBStick
* leds.py    : gestion du rack de leds
* main.py    : script principaldu jeux
* pwm.py     : conçu par [MC Hobby](https://github.com/mchobby/pyboard-driver/tree/master/PYBStick) : gestion des sorties PWM de la PYBStick


## synoptique du jeux
Un message d'accueil avec musique apparait, ainsi qu'une petite animation colorée des leds.

![intro](_docs/Ecran_01_accueil.png)

Le joueur est ensuite invité à choisir un mode de jeux:
* __Vert__ : facile. De nouvelles séquences de 3 portes à ouvrir sont rajoutées sans modifier les précédentes. Chaque porte est associée à un son.
* __Bleu__ : moyen, idem que le mode vert mais sans les sons
* __Jaune__: difficile. Dans ce mode, la séquence de portes à ouvrir est réinitialisée au hasard depuis le début, avec les sons activés.
* __Rouge__: expert. Idem mode Jaune mais sans les sons.

![choix mode](_docs/Ecran_02_mode.png)

Le mode choisi est confirmé sur l'écran LCD

![confirmation](_docs/Ecran_03_modeChoisi.png)

Le joueur est alors invité à :
* observer la séquence de 3 portes (avec ou sans son, selon le mode choisi) à ouvrir, indiquée par le guide
* reproduire la même séquence à l'aide du rack de boutons poussoir

S'il gagne: la led verte va clignoter 3 fois, une clé est trouvée, et si le record du mode est battu il est aussi mis à jour.

![confirmation](_docs/Ecran_04_niveau.png)

S'il se trompe, vous êtes perdu dans le labyrinthe de la PybStick! Une musique de la loose est jouée, la led rouge clignote 3 fois, et un message est indiqué sur l'écran.  Le jeux retourne alors sur l'écran de choix du mode.

![loose](_docs/Ecran_05_loose.png)

Si vous avez trouvé les 10 clés: bravo et respect !

![bravo](_docs/Ecran_06_BRAVO.png)



