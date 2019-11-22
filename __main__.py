from time import *
import I2C_LCD_driver
import psutil
import sys


# Converted 11111, 11110, 11100, 11000, 10000, 00000 to hex for the partial blocks
fontdata = [
    [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10],
    [0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18],
    [0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C],
    [0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E],
    [0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F],
]

mylcd = I2C_LCD_driver.lcd()
mylcd.lcd_load_custom_chars(fontdata)

while True:
    sleep(0.2)
    mylcd.lcd_write(0x80)  # Move the cursor to the top left

    cpu_usage = int(psutil.cpu_percent())  #  cpu_percent is a float, convert to int

    usage = int(cpu_usage / 1.2)  # Only 80 segments on the display, scale to fit

    blocks = int(usage / 5)  # How many "full" blocks to show
    remainder = int((usage % 5)) # And the number of columns to light up on the partial blocks

    # Draw tall the "full" blocks
    for i in range(0, blocks):
        mylcd.lcd_write_char(5)

    # And then the partial one
    mylcd.lcd_write_char(remainder)

    # Fill the rest of the line with white space so as to erase whatever was there before
    for i in range(blocks + 1, 16):
        mylcd.lcd_write_char(0)

    # On the line below, write the CPU utilization.
    mylcd.lcd_display_string(f"CPU: {cpu_usage}%   ", line=2)  # Extra spaces at the end to clear the line
