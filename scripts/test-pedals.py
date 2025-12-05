#!/usr/bin/python3
from gpiozero import Button, LED
from time import time, sleep

# GPIO pins
btnA = Button(17, pull_up=True, bounce_time=0.05)
btnB = Button(27, pull_up=True, bounce_time=0.05)

ledA = LED(22)
ledB = LED(23)

A_down_time = None
B_down_time = None

print("")
print("==============================================")
print("    ReCure Teleprompter — Pedal Test Mode")
print("==============================================")
print("A = GPIO17  (TIP)")
print("B = GPIO27  (RING)")
print("Press pedals to see clean event logs.")
print("LEDs mirror button state. Ctrl+C to exit.")
print("==============================================")
print("")

# ---------- Handlers ----------

def A_pressed():
    global A_down_time
    A_down_time = time()
    ledA.on()
    print("[A] PRESSED")

def A_released():
    global A_down_time
    held = time() - A_down_time if A_down_time else 0
    ledA.off()
    print(f"[A] RELEASED (held {held:.3f}s)")
    A_down_time = None

def B_pressed():
    global B_down_time
    B_down_time = time()
    ledB.on()
    print("[B] PRESSED")

def B_released():
    global B_down_time
    held = time() - B_down_time if B_down_time else 0
    ledB.off()
    print(f"[B] RELEASED (held {held:.3f}s)")
    B_down_time = None

# Bind events
btnA.when_pressed = A_pressed
btnA.when_released = A_released
btnB.when_pressed = B_pressed
btnB.when_released = B_released

# ---------- Main Loop ----------
try:
    while True:
        sleep(0.02)
except KeyboardInterrupt:
    print("\nExiting pedal test mode.")
