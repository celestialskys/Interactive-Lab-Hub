# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
import time
import board
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility
import color_api
import digitalio

i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_color = True

buttonA = digitalio.DigitalInOut(board.D23)    # GPIO23 (PIN 16)
buttonB = digitalio.DigitalInOut(board.D24)    # GPIO24 (PIN 18)
# Use internal pull-ups; buttons then read LOW when pressed.
buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB.switch_to_input(pull=digitalio.Pull.UP)
items = []

    
def getColors():
    # wait for color data to be ready
    my_color_data = {}
    if apds.color_data_ready:
        # get the data and print the different channels
        r, g, b, c = apds.color_data
        r_norm = (r / c) * 255
        g_norm = (g / c) * 255
        b_norm = (b / c) * 255
        
        a = c / 65535.0 #asked ChatGPT to help me create an alpha value from clear channel
       
        my_color_data = {"rgba_values": {"r": r_norm, "g": g_norm, "b": b_norm, "a": a}, "color_temp": colorutility.calculate_color_temperature(r, g, b), "light_lux": colorutility.calculate_lux(r, g, b)}
    return(my_color_data)

def main():
    print("Welcome please click top button to begin checking your outfit")
    while True:
        a_pressed = (buttonA.value == False)
        b_pressed = (buttonB.value == False)
        if a_pressed:
            print("Checking your outfit")
            items.append(getColors())
            # print(items[-1:][0]["rgba_values"])
            # print(color["rgba_values"])
            match = color_api.get_name_by_rgba(items[-1:][0]["rgba_values"])
            # print(f"Your outfit is {match['name']} with hex {match['hex']}")
            time.sleep(1)
        if b_pressed:
            print("Exiting program")
            break
        time.sleep(0.1)
        
if __name__ == "__main__":
    main()

    