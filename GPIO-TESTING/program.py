"""
export BLINKA_FT232H=1
"""


import os
import time
import board
import subprocess
from rainbowio import colorwheel
from adafruit_seesaw import seesaw, neopixel, rotaryio, digitalio
import adafruit_character_lcd.character_lcd_i2c as character_lcd



lcd_columns = 16
lcd_rows = 2



i2c = board.I2C()
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)
seesaw = seesaw.Seesaw(i2c, 0x36)



############ LCD ############
# lcd.clear()
lcd.backlight = True
# lcd.text_direction = lcd.LEFT_TO_RIGHT
# lcd.cursor = False
lcd.cursor = True
# lcd.blink = False

credits = 0

# lcd.message = f"Credits: {credits}"

# C = [14,27,24,24,24,27,14,0]
# R = [15,25,25,15,11,11,25,0]
# E = [31,1,1,15,1,1,31,0]
# D = [15,25,25,25,25,25,15,0]
# I = [31,4,4,4,4,4,31,0]
# T = [31,4,4,4,4,4,4,0]
# S = [30,1,1,14,16,16,15,0]

# lcd.create_char(0, C)
# lcd.create_char(1, R)
# lcd.create_char(2, E)
# lcd.create_char(3, D)
# lcd.create_char(4, I)
# lcd.create_char(5, T)
# lcd.create_char(6, S)

print("done creating chars")

dink = "aplay /home/satoshi/lnarcade/lnarcade/resources/sounds/dink.wav"
# dink = "/usr/bin/aplay /home/satoshi/lnarcade/lnarcade/resources/sounds/dink.wav"


encoder = rotaryio.IncrementalEncoder(seesaw)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
switch = digitalio.DigitalIO(seesaw, 24)

pixel = neopixel.NeoPixel(seesaw, 6, 1)
pixel.brightness = 0.5

last_position = -1
color = 0

# Get current volume from the system
volume_query = os.popen("amixer get 'Master' | grep -m1 -o [0-9]*% | tr -d %").read().strip()
current_volume = int(volume_query)

while True:
    position = -encoder.position

    if position != last_position:
        print(position)

        # Change the LED color.
        if position > last_position:
            color += 1
            current_volume = min(100, current_volume + 5)  # increase by 5%

        else:
            color -= 1
            current_volume = max(0, current_volume - 5)  # decrease by 5%

        color = (color + 256) % 256
        pixel.fill(colorwheel(color))

        # Adjust system volume using the 'amixer' command
        v = f"amixer set 'Master' -- {current_volume}%"
        print(v)
        print(os.system( v ))
        # ch = subprocess.Popen( v )

        os.system( dink )
        # proc = subprocess.Popen( dink )



        # lcd.clear()
        # lcd.message = f"{current_volume}"

    last_position = position
