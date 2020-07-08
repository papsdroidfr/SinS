#################################################################
#
# Auteur : papsdroid - https://www.papsdroid.fr
# Version: Juin 2020
# script MicoPython principal du jeux SinS sur PYBStick26
#
################################################################"

from leds import RackLeds
from lcd import Lcd
from buzzer import Buzz
from buttons import RackButtons
from random import randint, seed
import time, os

class Jeux_sins():
    """ classe gestion du jeux  """
    def __init__(self):
        """ constructeur """
        print ('Démarrage jeux ... ')
        self.lcd = Lcd()                # affichage LCD du jeux
        self.lcd.write_char('robot_ok', pos=(0,0) )
        self.lcd.msg_centre('SinS', 'Initialisation')
        self.lcd.write_char('robot_ok', pos=(15,0) )
        self.buzzer=Buzz()              # buzzer du jeux
        self.rackleds=RackLeds()        # rack de leds
        self.rackbuttons=RackButtons(self.rackleds, self.buzzer)  # rack de boutons
        self.color = ['V','B','J','R']  # couleur du jeux
        self.dic_color = {'V':0, 'B':1, 'J':2, 'R':3}
        self.file_scores = '/flash/scores.txt' # fichier des records
        self.scores = self.read_scores() # dictionnaire des record
        self.total_keys=10               # nb_clés à trouver   

        #mode de difficulté du jeux
        self.dic_mode = {
            'V': ['Vert',  'Facile']    ,
            'B': ['Bleu',  'Moyen']     ,
            'J': ['Jaune', 'Difficile'] ,
            'R': ['Rouge', 'Expert']    , 
            }
        self.mode = 'V'

        self.nb_portes=3              # nb de portes par niveau à ouvrir
        self.niveau = self.nb_portes  # nb de leds dans la séquence en cours
        self.init_seq()               # initialise séquences

    def init_seq(self):
        """ réinitialise les séquences à vide"""
        self.seq_led_droid = []
        self.seq_led_joueur = []
        seed(randint(0,32000))  #initialize random number generator

    def add_seq(self):
        """ ajoute une séquence de nb_portes aléatoires au jeux"""
        for _ in range(self.nb_portes):
            self.seq_led_droid.append(self.color[randint(0,3)])
        
            
    def nouvelle_seq(self):
        """ détermine la nouvelle séquence de couleurs à trouver"""
        self.seq_led_joueur = []    # remise à zéro de la séquence du joueur
        if self.mode in ['J','R']:  # séquences aléatoires depuis le début
            self.seq_led_droid = []
            for n in range(self.niveau//self.nb_portes):
                self.add_seq()
        else:  # sinon on ajoute nb_portes couleurs au hasard
            self.add_seq()
    
    def add_sequence_joueur(self, color):
        """ ajoute la couleur jouée par le joueur"""
        self.seq_led_joueur.append(color)
        
    def read_scores(self):
        """ retourne le dictionaires des records à battre par mode V,B,J,R"""
        dic_scores = {'V':0, 'B':0, 'J':0, 'R':0} #scores par niveaux
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
    
    def loop(self):
        """ boucle principale du jeux"""
        while True :
            #initialisations
            self.init_seq()            
            self.niveau=self.nb_portes 
            self.lcd.clear()
            self.rackbuttons.desactivate_buzzer()
            self.lcd.msg_centre('Choix du mode', 'Quelle couleur ?' )
            
            # choix du mode de jeux
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
                #self.lcd.msg('Niveau:'+str(self.niveau), 'Record:'+ str(self.scores[self.mode]))
                self.lcd.msg('Niveau:', 'Record:')
                self.lcd.write_key(self.niveau//self.nb_portes, 0) # niveau
                self.lcd.write_key(self.scores[self.mode], 1)      # record du mode joué
                time.sleep(1)

                #affichage de la séquence à trouver
                for rang, color in enumerate(self.seq_led_droid):
                    self.rackleds.get_led(color).smooth_on()  # led allumée
                    if self.mode in ['V','J']:
                        self.buzzer.buzzId(color)       # son correspondant à la couleur uniquement pour les modes V et J
                    time.sleep(0.5)                     # temps d'attente en 2 leds
                    self.buzzer.mute()                  # buzzer mute
                    self.rackleds.get_led(color).smooth_off()  # led éteinte
                    time.sleep(0.5)                            # temps d'attente
                    if (rang+1)%self.nb_portes == 0:     # attente supplémentaires entre 2 séries de nb_portes
                        time.sleep(0.3)
                        
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
                    if (self.scores[self.mode] < self.niveau//self.nb_portes): # le record du mode est battu
                        self.scores[self.mode]=self.niveau//self.nb_portes     # maj du dictionnaire des records
                        self.write_scores(self.scores)          # enregistrement des records
                    if self.niveau == self.total_keys*self.nb_portes:
                        # toutes les clés sont trouvées
                        self.buzzer.welcome_sound()
                        self.lcd.clear()
                        self.lcd.msg_centre('BRAVO!')
                        self.lcd.write_char('robot_ok', pos=(0,0) )
                        self.lcd.write_char('robot_ok', pos=(15,0) )
                        for n in range(10):
                            self.lcd.write_char('key', pos=(3+n,1) )
                            time.sleep(0.3)
                        time.sleep(2)
                        continuer = False
                    else:
                        self.niveau += self.nb_portes
                else:
                    #print('Perdu!')
                    self.lcd.clear()
                    self.lcd.msg_centre('Et non!')
                    for l in range(6,9):
                        self.lcd.write_char('robot_ko', pos=(l,1))
                    self.buzzer.loose_sound()
                    self.rackleds.loose()    # animation perdu
                    time.sleep(1)
                    continuer = False

#script du jeux
#----------------------------------------------
jeux=Jeux_sins()
jeux.loop()

