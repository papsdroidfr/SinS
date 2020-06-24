#################################################################
#
# Auteur : papsdroid - https://www.papsdroid.fr
# Version: Juin 2020
# classe gestion du rack de leds du jeux sins, sur PYBStick26
#
#################################################################
from pwm import *
from time import sleep

class Led:
    """défini une led pour le jeux SimonStick
    """
    def __init__(self, color, pin):
        """ constructeur
                color = 'V', 'B', 'J', 'R'
                pin = 'S8', 'S10', 'S12', ou 'S16'
        """
        self.color=color    # led color 
        self.pwm = pwm(pin) # led pin 

    def on(self):
        """ allume la led """
        self.pwm.percent=100
        
    def smooth_on(self, delay=0.001):
        """ allume la led en variant la luminosité par pas de step"""
        for p in range(101):
            self.pwm.percent=p
            sleep(delay)

    def off(self):
        """ étteind la led """
        self.pwm.percent=0
        
    def smooth_off(self,delay=0.001):
        """ étteind la led en variant la luminosité par pas de step"""
        for p in range(100,-1,-1):
            self.pwm.percent=p
            sleep(delay)
    
    def clignote(self, n):
        """fait clignoter la led n fois"""
        for x in range(n):
            self.smooth_on()
            sleep(0.1)
            self.smooth_off()
            sleep(0.1)
            

class RackLeds:
    """ classe qui défini un rack de 4 leds pour le jeux SimonStick"""
    def __init__(self):
        self.color=['V', 'B' , 'J', 'R']
        self.rang_color = {'V':0, 'B':1, 'J':2, 'R':3}
        self.dic_leds = {'V': 'S8',  # 'color' : 'pin'
                         'B': 'S10',
                         'J': 'S12',
                         'R': 'S16'
            }

        self.leds = []   #liste des leds du rack
        for color in self.color:
            self.leds.append(Led(color=color, pin=self.dic_leds[color]))
        self.animation_demarrage()

    def get_led(self,color):
        """ retourne la led de couleur 'color' """
        return self.leds[self.rang_color[color]] 
        
    def off(self):
        """étteind tout le rack de leds"""
        for l in self.leds:
            l.off()

    def smooth_off(self, delay=0.001):
        """etteind le rack le led avec un effet variateur"""
        for p in range(100,-1,-1):
            for l in self.leds:
                l.pwm.percent=p
            sleep(delay)

    def on(self):
        """ allume toutes les leds"""
        for l in self.leds:
            l.on()

    def smooth_on(self, delay=0.001):
        """ allume les leds avec un effet variateur"""
        for p in range(101):
            for l in self.leds:
                l.pwm.percent=p
            sleep(delay)

    def wave(self):
        """allume les leds une par une dans un sens, puis dans l'autre"""
        for l in self.leds: #allumage des leds vers la droite
            l.on()
            sleep(0.1)
            l.off()
        for l in self.leds[::-1]: #allumage des leds vers la gauche
            l.on()
            sleep(0.1)
            l.off()

    def clignote(self):
        """fait clignoter toutes les leds toutes en même temps"""
        self.smooth_on()
        sleep(0.05)
        self.smooth_off()
        sleep(0.05)

    def animation_demarrage(self):
        """ animation de démarrage"""
        for x in range(3):
            self.wave()
        for x in range(3):
            self.clignote()
            
    def win(self):
        """ animation lorsqu'un tour est gagné"""
        self.leds[0].clignote(3)    #clignoter la led verte 3 fois
    
    def lose(self):
        """ animation lorsqu'un tour est perdu"""
        self.leds[3].clignote(3)    #clignoter la led rouge 3 fois
