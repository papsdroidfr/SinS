#################################################################
#
# Auteur : papsdroid - https://www.papsdroid.fr
# Version: Juin 2020
# Classe gestion du Buzzer du jeux LabyStick sur PYBStick26
#
################################################################"

from machine import Pin
from pyb import Timer
from time import sleep

class Buzz():
    def __init__(self):
        """ constructeur, par défaut buzzerOn=False: non activé"""
        self.level=25        # niveau sonnore 0 (off) à 100 (max)
        self.freq_lam7 = [440, 523, 659, 784] #les bluesman vont reconnaître un accord de Lam7
        self.dic_freq={ 'V': 440, # fréquence ledG = La
                        'B': 523, # fréquence ledB = Do
                        'J': 659, # fréquence ledY = Mi
                        'R': 784  # fréquence ledR = Sol
                       }
        self.pin='S5'       # buzzer commandé par pin s5: Timer n°4, channel n°3 
        self.timer = Timer(4, freq=self.dic_freq['V'])
        self.channel = self.timer.channel(3,Timer.PWM, pin=Pin(self.pin))
        self.mute()
        self.welcome_sound()
        
    def mute(self):
        """ arrête le buzzer"""
        self.channel.pulse_width_percent(0)

    def play(self):
        """ active le buzzer, volume de 0 à 100"""
        self.channel.pulse_width_percent(self.level%101)
        
    def chg_freq(self, freq=500):
        """ modifie la fréquence du buzzer pour changer de note
        Table des fréquences par note/octave:
             0       1      2      3      4      5      6      7      8      9
        do   32.703  65.406 130.81 261.63 523.25 1046.5 2093.  4186.  8372.  16744.
        do#  34.648  69.296 138.59 277.18 554.37 1108.7 2217.5 4434.9 8869.8 17740.
        ré   36.708  73.416 146.83 293.66 587.33 1174.7 2349.3 4698.6 9397.3 18795.
        ré#  38.891  77.782 155.56 311.13 622.25 1244.5 2489.  4978.  9956.1 19912.
        mi   41.203  82.407 164.81 329.63 659.26 1318.5 2637.  5274.  10548. 21096.
        fa   43.654  87.307 174.61 349.23 698.46 1396.9 2793.8 5587.7 11175. 22351.
        fa#  46.249  92.499 185.   369.99 739.99 1480.  2960.  5919.9 11840. 23680.
        sol  48.999  97.999 196.   392.   783.99 1568.  3136.  6271.9 12544. 25088.
        sol# 51.913  103.83 207.65 415.3  830.61 1661.2 3322.4 6644.9 13290. 26580.
        la   55.     110.   220.   440.   880.   1760.  3520.  7040.  14080. 28160.
        la#  58.27   116.54 233.08 466.16 932.33 1864.7 3729.3 7458.6 14917. 29834.
        si   61.735  123.47 246.94 493.88 987.77 1975.5 3951.1 7902.1 15804. 31609.
        """
        self.timer.freq(freq)
            
    def buzzId(self, color):
        """fait sonner le buzzer avec une fréquence correspond à color
           color dans la liste ['green', 'blue','yellow', 'red']
        """
        self.chg_freq(self.dic_freq[color]) # modifie la fréquence du timer
        self.play()                         # active le son du buzzer

    def welcome_sound(self):
        """ joue un accord de Lam7"""    
        for freq in self.freq_lam7:
            self.chg_freq(freq)
            self.play()
            sleep(0.1)
        self.mute()

    def lose_sound(self):
        """ joue un accord de Lam7 à l'envers"""       
        for freq in self.freq_lam7[::-1]:
            self.chg_freq(freq)
            self.play()
            sleep(0.08)
        self.mute()
            
