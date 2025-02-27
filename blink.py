# blink.py
from machine import Pin
import time

# Pico has a built-in LED connected to GP25
led = Pin(25, Pin.OUT)

while True:
    led.value(1)  # LED on
    time.sleep(0.5)
    led.value(0)  # LED off
    time.sleep(2.5)
