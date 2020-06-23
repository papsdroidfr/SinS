# SimonStick
Jeux de mémoire SIMON à base d'une PYBStick26

## matériel nécessaire
* 1 PYBStick26
* 4 leds 5mm (Verte, Bleue, Jaune, Rouge)
* 4 résistances 220 ohms (pour les leds)
* 1 transistor npn
* 1 résistance 1k ohms (pour le transistor)
* 1 petit buzzer actif
* 4 petits boutons poussoir 6mm
* 1 écran LCD 1602 avec backpack I2C

## prototypage sur breadboard

[_docs/SimonStick26_bb.png]

## scipts micropython à installer sur la PYBStick
dans le répertoire PYBFLASH qui s'affiche à l'odinateur lors du branchement de la PYBStick sur un port USB, déposez tous les * fichiers Micropython:
* buttons.py : gestion du rack de boutons poussoirs
* buzzer.py  : gestion du buzzer
* lcd.py     : gestion du LCD
* lcd2ic.py  : conçu par MC Hobby: gestion du LCD via I2C de la PYBStick
* leds.py    : gestion du rack de leds
* main.py    : script principal 
* pwm.py     : conçu par MC Hobby: gestion des sorties PWM de la PYBStick
