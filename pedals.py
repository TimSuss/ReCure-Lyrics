#!/usr/bin/python3
from gpiozero import Button, LED
from time import time, sleep
from subprocess import run

# GPIO pins
btnA = Button(17, pull_up=True)
btnB = Button(27, pull_up=True)

ledA = LED(22)
ledB = LED(23)

# State
A_down_time = None
B_down_time = None
diagnostic_mode = False
last_combo_time = 0

# ------------- Key Helpers (Wayland safe) -----------------

def keypress(keyname):
    run(["wtype", "-k", keyname])

def page_up():
    keypress("Page_Up")

def page_down():
    keypress("Page_Down")

def send_tab():
    keypress("Tab")

# ------------- Diagnostic Mode ----------------------------

def enter_diagnostic():
    global diagnostic_mode
    diagnostic_mode = True
    print("Diagnostic mode ON")

def exit_diagnostic():
    global diagnostic_mode
    diagnostic_mode = False
    ledA.off()
    ledB.off()
    print("Diagnostic mode OFF")

# ------------- Button Handlers ----------------------------

def A_pressed():
    global A_down_time
    A_down_time = time()

def A_released():
    global A_down_time

    if diagnostic_mode:
        ledA.off()
        A_down_time = None
        return

    # Tap = PAGE UP
    if A_down_time and (time() - A_down_time) < 0.4:
        page_up()

    A_down_time = None

def B_pressed():
    global B_down_time
    B_down_time = time()

def B_released():
    global B_down_time

    if diagnostic_mode:
        ledB.off()
        B_down_time = None
        return

    # Tap = PAGE DOWN
    if B_down_time and (time() - B_down_time) < 0.4:
        page_down()

    B_down_time = None

btnA.when_pressed = A_pressed
btnA.when_released = A_released
btnB.when_pressed = B_pressed
btnB.when_released = B_released

# ------------- Main Loop ----------------------------------

while True:
    now = time()

    # A hold 5 sec → diagnostic mode toggle
    if A_down_time:
        if (now - A_down_time) >= 5:
            if not diagnostic_mode:
                enter_diagnostic()
            else:
                exit_diagnostic()

    # Press both briefly → TAB
    if btnA.is_pressed and btnB.is_pressed:
        if now - last_combo_time > 0.5:
            send_tab()
            last_combo_time = now

    # Diagnostic LED mirrors button state
    if diagnostic_mode:
        ledA.on() if btnA.is_pressed else ledA.off()
        ledB.on() if btnB.is_pressed else ledB.off()

    sleep(0.02)
