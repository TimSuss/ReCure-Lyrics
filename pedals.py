#!/usr/bin/python3
from gpiozero import Button, LED
from time import time, sleep
from subprocess import run

# ------------------------------
# GPIO Setup
# ------------------------------
btnA = Button(17, pull_up=True)
btnB = Button(27, pull_up=True)

ledA = LED(22)
ledB = LED(23)

# ------------------------------
# Timing state
# ------------------------------
A_down_time = None
B_down_time = None
diagnostic_mode = False

# ------------------------------
# Helper functions
# ------------------------------
def keypress(scancode):
    run(["ydotool", "key", scancode])

def page_down():
    keypress("0xFF56")

def slow_scroll():
    keypress("0xFF54")   # Down arrow

def jump_to_top():
    keypress("0xFF50")   # Home

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

# ------------------------------
# Button event handlers
# ------------------------------

def A_pressed():
    global A_down_time
    A_down_time = time()

def A_released():
    global A_down_time

    if diagnostic_mode:
        ledA.off()
        return

    if A_down_time:
        held = time() - A_down_time
        if held < 0.5:  # short tap
            page_down()

    A_down_time = None

def B_pressed():
    global B_down_time
    B_down_time = time()

def B_released():
    global B_down_time

    if diagnostic_mode:
        ledB.off()
        return

    if B_down_time:
        held = time() - B_down_time
        if held < 0.5:
            slow_scroll()

    B_down_time = None

# ------------------------------
# Assign handlers
# ------------------------------
btnA.when_pressed = A_pressed
btnA.when_released = A_released
btnB.when_pressed = B_pressed
btnB.when_released = B_released

# ------------------------------
# Main loop: detect holds + combos
# ------------------------------
while True:
    now = time()

    # Diagnostic mode (hold A 5 seconds)
    if A_down_time and not diagnostic_mode:
        if now - A_down_time >= 5:
            enter_diagnostic()

    # Diagnostic mode exit (hold A 5 seconds again)
    if A_down_time and diagnostic_mode:
        if now - A_down_time >= 5:
            exit_diagnostic()

    # Diagnostic LED behavior
    if diagnostic_mode:
        if btnA.is_pressed:
            ledA.on()
        else:
            ledA.off()

        if btnB.is_pressed:
            ledB.on()
        else:
            ledB.off()

    # Combo hold (A + B 3 seconds)
    if A_down_time and B_down_time and not diagnostic_mode:
        if now - A_down_time >= 3 and now - B_down_time >= 3:
            jump_to_top()
            A_down_time = None
            B_down_time = None

    sleep(0.02)
