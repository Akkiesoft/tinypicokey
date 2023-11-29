# Written in CircuitPython
# for Raspberry Pi Pico or Pimoroni Tiny2040

import board
from digitalio import DigitalInOut, Direction, Pull
from time import sleep
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

led = (
    DigitalInOut(board.LED_R),
    DigitalInOut(board.LED_G),
    DigitalInOut(board.LED_B)
)
for l in led:
    l.direction = Direction.OUTPUT
    # tiny2040 LED is active low
    l.value = 1

keyboard = 0
while not keyboard:
    try:
        keyboard = Keyboard(usb_hid.devices)
        layout = KeyboardLayoutUS(keyboard)
    except:
        pass
    sleep(1)

keycodes = (
    ("Hello", Keycode.ENTER),
    (Keycode.A,),
    (Keycode.B,),
)
button = (
    DigitalInOut(board.GP4),
    DigitalInOut(board.GP5),
    DigitalInOut(board.GP6)
)
for b in button:
    b.switch_to_input(pull=Pull.UP)
sw = [0] * len(button)

def send_key(key):
    repeat_block = False
    try:
        for k in key:
            if (type(k) is str):
                repeat_block = True
                layout.write(k)
            else:
                keyboard.press(k)
            sleep(0.05)
        if repeat_block:
            keyboard.release_all()
    except:
        pass

while True:
    for i,b in enumerate(button):
        if not b.value:
            if not sw[i]:
                send_key(keycodes[i])
                sw[i] = 1
                led[i].value = 0
        else:
            if sw[i]:
                keyboard.release_all()
                sw[i] = 0
                for l in led:
                    l.value = 1
