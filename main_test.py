from machine import I2C
from lcdi2c import LCDI2C
from pwm import *
from time import sleep


# Initialise l'ecran LCD
i2c = I2C(2)
lcd = LCDI2C( i2c, cols=16, rows=2 )
lcd.backlight()

# Affiche un messagee (sans retour à la ligne automatique)
lcd.print("Hello, from MicroPython !")
sleep( 2 )
# Défillement horizontal
for i in range( 10 ):
	lcd.scroll_display()
	sleep( 0.500 )

# Contrôle du rétro-éclairage
for i in range( 3 ):
	lcd.backlight(False)
	sleep( 0.400 )
	lcd.backlight()
	sleep( 0.400 )

# Effacer l'écran
lcd.clear()

# Déplacer le curseur + affichage
lcd.set_cursor( (4, 1) ) # Tuple avec Col=4, Row=1, index de 0 à N-1
lcd.print( '@' )
# ou faire un positionnage + affichage avec un seul appel à print()
lcd.print( '^', pos=(10,0) )
lcd.print( '!', pos=(10,1) )
sleep( 2 )

# Effacer l'écran
lcd.clear()
lcd.home()  # Curseur à la position "home"
lcd.cursor() # Afficher curseur
lcd.blink()  # Curseur clignotant
lcd.print( "Cursor:" )

#leds PWM
p_green = pwm('S8')
p_blue = pwm('S10')
p_yellow = pwm('S12')
p_red = pwm('S16')

percent=0
step = 1
while True:
    p_green.percent = percent
    p_blue.percent = percent
    p_yellow.percent = percent
    p_red.percent = percent
    sleep(0.01)
    percent = (percent+step)%101
    if percent==100 or percent==0:
            step=-step
    
