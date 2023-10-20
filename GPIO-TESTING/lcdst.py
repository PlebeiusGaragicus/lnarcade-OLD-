import time

import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd
i2c = busio.I2C(board.SCL, board.SDA)
cols = 16
rows = 2
lcd = character_lcd.Character_LCD_I2C(i2c, cols, rows)

lcd.message = "Hello\nCircuitPython!"

time.sleep(5)

# import board
# import busio
# import digitalio
# import adafruit_character_lcd.character_lcd_spi as character_lcd
# spi = busio.SPI(board.SCK, MOSI=board.MOSI)
# latch = digitalio.DigitalInOut(board.D5)
# cols = 16
# rows = 2
# lcd = character_lcd.Character_LCD_SPI(spi, latch, cols, rows)
# lcd.message = "Hello\nCircuitPython!"