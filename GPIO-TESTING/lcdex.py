# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for 16x2 character lcd connected to an MCP23008 I2C LCD backpack."""
import time
import board
import adafruit_character_lcd.character_lcd_i2c as character_lcd

lcd_columns = 16
lcd_rows = 2

i2c = board.I2C()
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

lcd.clear()
lcd.backlight = True
lcd.text_direction = lcd.LEFT_TO_RIGHT
lcd.cursor = False
lcd.blink = False

lcd.message = "Credits: 0"

while True:
    time.sleep(5.0)



# while True:
#     # Print a two line message
#     lcd.message = "Hello\nCircuitPython"
#     # Wait 5s
#     time.sleep(5)
#     lcd.clear()
#     # Print two line message right to left
#     lcd.text_direction = lcd.RIGHT_TO_LEFT
#     lcd.message = "Hello\nCircuitPython"
#     # Wait 5s
#     time.sleep(5)
#     # Return text direction to left to right
#     lcd.text_direction = lcd.LEFT_TO_RIGHT
#     # Display cursor
#     lcd.clear()
#     lcd.cursor = True
#     lcd.message = "Cursor! "
#     # Wait 5s
#     time.sleep(5)
#     # Display blinking cursor
#     lcd.clear()
#     lcd.blink = True
#     lcd.message = "Blinky Cursor!"
#     # Wait 5s
#     time.sleep(5)
#     lcd.blink = False
#     lcd.clear()
#     # Create message to scroll
#     scroll_msg = "<-- Scroll"
#     lcd.message = scroll_msg
#     # Scroll message to the left
#     for i in range(len(scroll_msg)):
#         time.sleep(0.5)
#         lcd.move_left()
#     lcd.clear()
#     lcd.message = "Going to sleep\nCya later!"
#     time.sleep(5)
#     # Turn backlight off
#     lcd.backlight = False