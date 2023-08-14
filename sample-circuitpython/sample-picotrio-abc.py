# Written in CircuitPython
# for Raspberry Pi Pico or Pimoroni Tiny2040

import board
from digitalio import DigitalInOut, Direction, Pull
from time import sleep
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

led = [
    DigitalInOut(board.LED_R),
    DigitalInOut(board.LED_G),
    DigitalInOut(board.LED_B)
]
for l in led:
    l.direction = Direction.OUTPUT
    # tiny2040 LED is active low
    l.value = 1

keyboard = 0
while not keyboard:
    try:
        keyboard = Keyboard(usb_hid.devices)
    except:
        pass
    sleep(1)

keycodes = [
    [Keycode.A],
    [Keycode.B],
    [Keycode.C]
]
button = [
    DigitalInOut(board.GP4),
    DigitalInOut(board.GP5),
    DigitalInOut(board.GP6)
]
for b in button:
    b.switch_to_input(pull=Pull.UP)
buttons = len(button)

released = 1
while True:
    no_push = 0
    for i,b in enumerate(button):
        if b.value:
            no_push += 1
            continue
        led[i].value = 0
        released = 0
        for k in keycodes[i]:
            keyboard.press(k)
            sleep(0.01)
    if no_push == buttons and not released:
        for l in led:
            l.value = 1
        keyboard.release_all()
        released = 1
