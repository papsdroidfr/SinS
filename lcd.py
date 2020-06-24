#################################################################
#
# Auteur : papsdroid - https://www.papsdroid.fr
# Version: Juin 2020
# classe gestion du LCD du jeux sins sur PYBStick26
#
#################################################################

from machine import I2C
from lcdi2c import LCDI2C
import time

class Lcd:
    def __init__(self):
        """ constructeur """
        try:
            self.i2c = I2C(2)
            self.lcd = LCDI2C( self.i2c, cols=16, rows=2 )
        except:
            print('I2C Address Error !')
            print('backpack LCD à brancher sur I2C(2) de la PYBStick26')
            print('SDA sur S11 et SCL sur S13')
            exit(1)
        #dictionnaire de caractères générés depuis https://maxpromer.github.io/LCD-Character-Creator/
        self.dic_chars= {'robot_ok': 0, 'robot_ko':1, 'key':2}
        chars = [ [0b01110,0b11111,0b10101,0b11111,0b11111,0b10001,0b11111,0b01110], # robot ok
                  [0b01110,0b11111,0b10101,0b11111,0b11111,0b11011,0b11111,0b01110], # robot ko
                  [0b11111,0b10001,0b01110,0b00100,0b00100,0b00110,0b00100,0b00111], # clé
                ]
        for n in range(len(chars)):
            self.lcd.create_char(n,chars[n])
        self.clear()
        self.lcd.backlight()  

    def clear(self):
        """ efface l'écran"""
        self.lcd.clear()
        
    def msg(self, lig1, lig2=''):
        """ affiche un message sur 2 lignes"""
        lig1, lig2 = lig1[:16], lig2[:16]
        self.lcd.print(lig1, pos=(0,0)) 
        self.lcd.print(lig2, pos=(0,1)) 

    def msg_centre(self, lig1, lig2=''):
        """ affiche un message centré, sur 2 lignes"""
        lig1, lig2 = lig1[:16], lig2[:16]
        self.lcd.print(lig1, pos=( (16-len(lig1))//2 ,0) ) 
        self.lcd.print(lig2, pos=( (16-len(lig2))//2 ,1) ) 

    def write_char(self, label, pos):
        """affiche le caractère spécial "label" en position pos(c,l)"""
        self.lcd.set_cursor(pos)
        self.lcd.write(self.dic_chars[label])

    def write_key(self, n, l):
        """affiche n trésors sur la ligne l"""
        self.lcd.set_cursor((16-n,l))
        for c in range(n):
            self.lcd.write(self.dic_chars['key'])
