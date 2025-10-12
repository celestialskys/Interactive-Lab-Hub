# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import color_api
from adafruit_apds9960.apds9960 import APDS9960
from adafruit_apds9960 import colorutility

i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_color = True

buttonA = digitalio.DigitalInOut(board.D23)    # GPIO23 (PIN 16)
buttonB = digitalio.DigitalInOut(board.D24)    # GPIO24 (PIN 18)
# Use internal pull-ups; buttons then read LOW when pressed.
buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB.switch_to_input(pull=digitalio.Pull.UP)
items = []


def main():
    print("Welcome please click top button to begin checking your outfit")
    while True:
        a_pressed = (buttonA.value == False)
        b_pressed = (buttonB.value == False)
        if a_pressed:
            print("Checking your outfit")
            colors = getColors()
            print(colors)
            match = color_api.get_closest_color(colors['r'], colors['g'], colors['b'])
            print(f"Your outfit is {match['name']} with hex {match['hex']}")
            time.sleep(1)
        if b_pressed:
            print("Exiting program")
            break
        time.sleep(0.1)

    
    
def getColors:
    # wait for color data to be ready
    while not apds.color_data_ready:
        time.sleep(0.005)

    # get the data and print the different channels
    r, g, b, c = apds.color_data
    # print("red: ", r)
    # print("green: ", g)
    # print("blue: ", b)
    # print("clear: ", c)

    # print("color temp {}".format(colorutility.calculate_color_temperature(r, g, b)))
    # print("light lux {}".format(colorutility.calculate_lux(r, g, b)))
    my_color_data = {r: r, g: g, b: b, a: c, "color_temp": colorutility.calculate_color_temperature(r, g, b), "light_lux": colorutility.calculate_lux(r, g, b)}
    return(my_color_data)
