#!/usr/bin/python3
from gpiozero import Button, LED
from time import time, sleep
from subprocess import run

# GPIO pins
btnA = Button(17, pull_up=True, bounce_time=0.05)
btnB = Button(27, pull_up=True, bounce_time=0.05)

ledA = LED(22)
ledB = LED(23)

# State
A_down_time = None
B_down_time = None
diagnostic_mode = False
A_hold_for_tab = False

SCROLL_MULTIPLIER = 10      # Number of arrow presses per pedal press
DEBOUNCE_RELEASE = 0.12     # Minimum press time before triggering

import sys

LOG_PATH = "/home/tim-r/pedal.log"

def log(msg):
    with open(LOG_PATH, "a") as f:
        f.write(msg + "\n")


# ----------------- Key Helpers -----------------

def keypress(keyname):
    run(["wtype", "-k", keyname])

def scroll_down():
    log("Scroll DOWN triggered")
    for _ in range(SCROLL_MULTIPLIER):
        run(["wtype", "-k", "Down"])

def scroll_up():
    log("Scroll UP triggered")
    for _ in range(SCROLL_MULTIPLIER):
        run(["wtype", "-k", "Up"])

def send_tab():
    keypress("Tab")


# ----------------- Diagnostic Mode -----------------

def enter_diagnostic():
    global diagnostic_mode
    diagnostic_mode = True
    print("\n===== DIAGNOSTIC MODE ON =====")
    ledA.blink(on_time=0.2, off_time=0.2)
    ledB.blink(on_time=0.2, off_time=0.2)

def exit_diagnostic():
    global diagnostic_mode
    diagnostic_mode = False
    ledA.off()
    ledB.off()
    print("\n===== EXITING DIAGNOSTIC MODE =====")

    # restart services
    run(["systemctl", "--user", "restart", "teleprompter.service"])
    run(["systemctl", "--user", "restart", "pedals.service"])


# ----------------- Button Handlers -----------------

def A_pressed():
    global A_down_time
    A_down_time = time()
    log("A pressed")

def A_released():
    global A_down_time, A_hold_for_tab

    if A_down_time is None:
        return

    held = time() - A_down_time

    # Enter/exit diagnostic
    if held >= 5:
        if not diagnostic_mode:
            enter_diagnostic()
        else:
            exit_diagnostic()
        A_down_time = None
        return

    # Long hold = enable TAB combo mode
    if held >= 0.4:
        A_hold_for_tab = True
        A_down_time = None
        return

    # Debounce short taps
    if held < DEBOUNCE_RELEASE:
        A_down_time = None
        return

    # Normal action
    if not diagnostic_mode:
        scroll_up()

    A_down_time = None

    ...
    log(f"A released (held {held:.3f}s)")
    ...

def B_pressed():
    global B_down_time
    B_down_time = time()
    log("B pressed")

def B_released():
    global B_down_time, A_hold_for_tab

    if B_down_time is None:
        return

    held = time() - B_down_time

    if held < DEBOUNCE_RELEASE:
        B_down_time = None
        return

    # TAB combo: A held, B tapped
    if A_hold_for_tab:
        send_tab()
        A_hold_for_tab = False
        B_down_time = None
        return

    # Normal scroll
    if not diagnostic_mode:
        scroll_down()

    B_down_time = None
    log(f"B released (held {held:.3f}s)")

btnA.when_pressed = A_pressed
btnA.when_released = A_released
btnB.when_pressed = B_pressed
btnB.when_released = B_released


# ----------------- Main Loop -----------------

while True:
    sleep(0.02)
