#################################################################
#
# Auteur : papsdroid - https://www.papsdroid.fr
# Version: Juin 2020
# Classe de gestion du rack de boutons du jeux SimonStick sur PYBStick26
#
################################################################"

from machine import Pin
from pyb import ExtInt
from time import sleep


class Button_led():
    def __init__(self, rackleds, rackbuttons, buzz, pin, color, id):
        self.rackleds = rackleds   
        self.rackbuttons = rackbuttons #rack auquel appartient le bouton
        self.buzzer = buzz     # buzzer du jeux 
        self.buttonPin=pin     # pin sur la PYBStick26
        self.color = color     # couleur du bouton (associé à la led de la même couleur)
        self.id = id           # rang dans le rack: 0 à 3
        self.button = Pin( pin, Pin.IN, Pin.PULL_UP ) # pin reliée au bouton en pull_up
        self.extint = ExtInt(pin, ExtInt.IRQ_FALLING, Pin.PULL_UP, self.callback)
        
    #fonction exécutée quand le bouton est préssé
    def callback(self, line):
        if not(self.rackbuttons.pressed):  #rien ne se passe si le rack est déjà en mode "bouton déjà pressé"
            sleep(0.05) # attente 50ms stabilisation: évite les rebonds
            if not(self.button.value()): # bouton toujours préssé après stabilisation
                self.rackbuttons.pressed = True
                #print('button ', self.color,' pressed')    
                self.rackbuttons.button_pressed = self.color
                self.rackleds.leds[self.id].smooth_on()  # allume la led correspondante au bouton
                if self.rackbuttons.buzzerActif:
                    self.buzzer.buzzId(self.color)       # fait sonner le buzzer avec la fréquence correspondante à la couleur
                sleep(0.5)
                self.rackleds.leds[self.id].smooth_off() # led etteinte
                self.buzzer.mute()                       # arrête le son du buzzer

class RackButtons():
    """ classe rack de 4 boutons de commande pour le jeux"""
    def __init__(self, rackleds, buzz):
        self.rackleds = rackleds
        self.buzzer=buzz
        self.buzzerActif = True
        self.buttons=[]
        self.buttons.append(Button_led(self.rackleds, self, self.buzzer, pin='S15', color='V',id=0)) # bouton LedG
        self.buttons.append(Button_led(self.rackleds, self, self.buzzer, pin='S19', color='B',id=1)) # bouton LedB
        self.buttons.append(Button_led(self.rackleds, self, self.buzzer, pin='S21', color='J',id=2)) # bouton LedY
        self.buttons.append(Button_led(self.rackleds, self, self.buzzer, pin='S23', color='R',id=3))  # bouton LedR
        self.pressed=False          # par défaut aucun bouton n'a été préssé

    def activate_buzzer(self):
        """active le buzzer"""
        self.buzzerActif=True
        
    def desactivate_buzzer(self):
        """désactive le buzzer"""
        self.buzzerActif=False
        
    

