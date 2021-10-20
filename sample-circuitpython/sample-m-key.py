# Written in CircuitPython
# for Raspberry Pi Pico or Pimoroni Tiny2040

import board
import digitalio
from time import sleep
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

keyboard=Keyboard(usb_hid.devices)
keycodes = [Keycode.M]

button = digitalio.DigitalInOut(board.GP6)
button.switch_to_input(pull=digitalio.Pull.UP)

led_r = digitalio.DigitalInOut(board.LED_R)
led_r.direction = digitalio.Direction.OUTPUT
led_g = digitalio.DigitalInOut(board.LED_G)
led_g.direction = digitalio.Direction.OUTPUT
led_b = digitalio.DigitalInOut(board.LED_B)
led_b.direction = digitalio.Direction.OUTPUT
# tiny2040 LED is active low
led_r.value = 1
led_g.value = 1
led_b.value = 1

while True:
  if not button.value:
    led_g.value = 0
    led_b.value = 0
    for k in keycodes:
      keyboard.press(k)
  else:
    led_g.value = 1
    led_b.value = 1
    keyboard.release_all()
  sleep(0.02)