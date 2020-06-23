#################################################################
#
# Auteur : papsdroid - https://www.papsdroid.fr
# Version: Juin 2020
# script MicoPython principal du jeux SimonStick sur PYBStick26
#
################################################################"

from leds import RackLeds
from lcd import Lcd
from buzzer import Buzz
from buttons import RackButtons
from random import randint
import time, os

class JeuxSimonStick():
    """ classe du jeux de mémoire SimonStick """
    def __init__(self):
        """ constructeur """
        print ('Démarrage jeux SimonStick ... ')
        self.lcd = Lcd()                # affichage LCD du jeux
        self.buzzer=Buzz()              # buzzer du jeux
        self.rackleds=RackLeds()        # rack de leds
        self.rackbuttons=RackButtons(self.rackleds, self.buzzer)  # rack de boutons de commande des leds
        self.color = ['V','B','J','R']  # couleur du jeux, et dictionnaire du rang des leds dans le rack
        self.dic_color = {'V':0, 'B':1, 'J':2, 'R':3}
        self.file_scores = '/flash/scores.txt' #fichier des records
        self.scores = self.read_scores()       # dictionnaire des record {'V':nv, 'B',nb ,'J',nj, 'R',nr}

        #mode de difficulté du jeux selon les couleurs
        """ V: séquence de leds de plus en plus longue, avec musique activée
            B: séquence de leds de plus en plus longue, sans musique
            Y: séquence de leds réinitialisées et plus longue à chaque fois, avec musique
            R: séquence de leds réinitialisées et plus longue à chaque tour, sans musique
        """
        self.dic_mode = {
            'V': ['Vert',  'Facile']    ,
            'B': ['Bleu',  'Moyen']     ,
            'J': ['Jaune', 'Difficile'] ,
            'R': ['Rouge', 'Expert']    , 
            }
        self.mode = 'V'                     # difficulté  choisie ('V' par défaut)

        self.niveau = 1           # niveau = nb de leds dans la séquence en cours
        self.seq_led_droid = []   # sequence des couleurs à retenir
        self.seq_led_joueur = []  # séquence des couleurs du joueur
        self.continuer = True     # fin de partie: continuer=False

    def init_seq(self):
        """ réinitialise les séquences à vide"""
        self.seq_led_droid = []
        self.seq_led_joueur = []
    
    def nouvelle_seq(self):
        """ détermine la nouvelle séquence de couleurs à trouver"""
        self.seq_led_joueur = []    # remise à zéro de la séquence du joueur
        if self.mode in ['J','R']:  # séquences totalement remaniées pour les modes 'J' et 'R'
            self.seq_led_droid = []
            for n in range(self.niveau):
                self.seq_led_droid.append(self.color[randint(0,3)])
        else:                       # sinon on ajoute juste une nouvelle couleur au hasard
            self.seq_led_droid.append(self.color[randint(0,3)])   
        #print('niveau:', self.niveau, 'sequence à trouver:', self.seq_led_droid)
    
    def add_sequence_joueur(self, color):
        """ ajoute la couleur jouée par le joueur"""
        self.seq_led_joueur.append(color)
        
    def read_scores(self):
        """ retourne le dictionaires des records à battre par mode V,B,J,R"""
        dic_scores = {'V':1, 'B':1, 'J':1, 'R':1} #scores par niveaux
        try:
            with open(self.file_scores, 'r') as f:
                for line in f.readlines():
                    l=line.strip()
                    mode,score = l[0], int(l[2:])
                    dic_scores[mode]=score
        except: #création du fichier score.txt s'il n'existe pas
            print('création fichier des scores')
            self.write_scores(dic_scores)
        print('record à battre par mode:', dic_scores)
        return dic_scores           
   
    def write_scores(self, scores):
        """ sauvegarde des record à battre"""
        with open(self.file_scores , 'w') as f:
            f.write('V:' + str(scores['V']) + '\n')
            f.write('B:' + str(scores['B']) + '\n')
            f.write('J:' + str(scores['J']) + '\n')
            f.write('R:' + str(scores['R']) + '\n')
        #print(os.listdir("/flash"))
            
    def loop(self):
        """ boucle principale du jeux"""
        while True :
            # initialisations
            self.init_seq()  # initialise les séquences à vide
            self.niveau=1    # démarre au niveau 1
            self.lcd.clear()
            self.rackbuttons.desactivate_buzzer()
            self.lcd.msg_centre('Choix du mode', 'Quelle couleur ?' )

            # choix du mode de jeux / difficulté: V(Facile,), B(moyen), J(difficile), R(expert)
            self.rackbuttons.pressed = False
            while not(self.rackbuttons.pressed): #attente appui sur un bouton du rack
                time.sleep(0.2)
            self.mode = self.rackbuttons.button_pressed
            self.lcd.clear()
            self.lcd.msg_centre('Tu as choisi', 'mode: '+self.dic_mode[self.mode][1] )
            if self.mode in ['V','J']:
                self.rackbuttons.activate_buzzer() #buzzer activé uniquement pour les modes V et J
            time.sleep(2)
            self.lcd.clear()

            #boucle de jeux tant que le joueur trouve la bonne séquence
            continuer = True
            while (continuer):
                #création d'une nouvelle séquence à trouver
                self.nouvelle_seq()    
                self.lcd.msg('Niveau:'+str(self.niveau), 'Record:'+ str(self.scores[self.mode]))
                time.sleep(1)
                #affichage de la séquence à trouver
                for color in self.seq_led_droid:
                    self.rackleds.get_led(color).smooth_on()  # led allumée
                    if self.mode in ['V','J']:
                        self.buzzer.buzzId(color)       # son correspondant à la couleur uniquement pour les modes V et J
                    time.sleep(0.5)                     # temps d'attente
                    self.buzzer.mute()                  # buzzer mute
                    self.rackleds.get_led(color).smooth_off()  # led éteinte
                    time.sleep(0.5)                            # temps d'attente
                #mémorisation séquence du joueur
                #print('à toi de jouer')
                self.rackbuttons.pressed = False
                for n in range(self.niveau):
                    #attente qu'un bouton du rack de boutons soit pressée
                    while not(self.rackbuttons.pressed):
                        time.sleep(0.2)
                    self.add_sequence_joueur(self.rackbuttons.button_pressed)
                    self.rackbuttons.pressed = False
                #print('Voici ton jeu: ', self.jeux.seq_led_joueur)
                #comparaison des listes
                self.rackbuttons.pressed = True #empêche la saisie sur une touche
                time.sleep(1)
                if (self.seq_led_joueur == self.seq_led_droid):
                    #print('Bien joué! niveau suivant')
                    self.rackleds.win()   #animation gagné
                    if (self.scores[self.mode]<self.niveau): # le record du mode est battu
                        self.scores[self.mode]=self.niveau   # maj du dictionnaire des records
                        self.write_scores(self.scores)       # enregistrement des records
                    self.niveau += 1
                else:
                    #print('Perdu!')
                    self.lcd.clear()
                    self.lcd.msg_centre('Et non!')
                    for l in range(6,9):
                        self.lcd.write_char('robot_ko', pos=(l,1))
                    self.buzzer.lose_sound()
                    self.rackleds.lose()    # animation perdu
                    time.sleep(1)
                    continuer = False


#script du jeux
#----------------------------------------------
jeux=JeuxSimonStick()
jeux.loop()

