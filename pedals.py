#!/usr/bin/python3
from gpiozero import Button, LED
from time import time, sleep
from subprocess import run, Popen

# GPIO pins
btnA = Button(17, pull_up=True, bounce_time=0.05)
btnB = Button(27, pull_up=True, bounce_time=0.05)

ledA = LED(22)
ledB = LED(23)

# State
A_down_time = None
B_down_time = None
diagnostic_mode = False

# Debounce timing
DEBOUNCE = 0.15

# For TAB combo: hold A then tap B
A_is_held_for_tab = False

# ------------- Key Helpers -----------------

def keypress(keyname):
    run(["wtype", "-k", keyname])

def page_up():
    keypress("Page_Up")

def page_down():
    keypress("Page_Down")

def send_tab():
    keypress("Tab")

# ------------- Diagnostic Mode -----------------

diagnostic_process = None

def enter_diagnostic():
    global diagnostic_mode, diagnostic_process

    diagnostic_mode = True
    ledA.on()
    ledB.on()
    print("Diagnostic mode ON")

    # Launch terminal window to print live states
    diagnostic_process = Popen([
        "lxterminal", "-e",
        "bash -c 'watch -n 0.1 \"gpiozero-pinout; echo; "
        "python3 - <<EOF\n"
        "import gpiozero, time\n"
        "A = gpiozero.Button(17, pull_up=True)\n"
        "B = gpiozero.Button(27, pull_up=True)\n"
        "while True:\n"
        "    print(f\"A: {A.is_pressed}  B: {B.is_pressed}\")\n"
        "    time.sleep(0.1)\n"
        "EOF\"'"
    ])

def exit_diagnostic():
    global diagnostic_mode, diagnostic_process

    diagnostic_mode = False
    ledA.off()
    ledB.off()

    print("Diagnostic mode OFF")

    if diagnostic_process:
        diagnostic_process.terminate()
        diagnostic_process = None

    # Restart services
    run(["systemctl", "--user", "restart", "teleprompter.service"])
    run(["systemctl", "--user", "restart", "pedals.service"])

# ------------- Button Handlers -----------------

def A_pressed():
    # Used only for measuring hold
    global A_down_time
    A_down_time = time()

def A_released():
    global A_down_time, A_is_held_for_tab

    if diagnostic_mode:
        ledA.off()
        return

    # Debounce
    if A_down_time and time() - A_down_time < DEBOUNCE:
        return

    # Check if A is being held for TAB combo
    if A_down_time and (time() - A_down_time) > 0.4:
        A_is_held_for_tab = True
        return

    # Normal PAGE UP action
    page_up()

    A_down_time = None

def B_pressed():
    global B_down_time
    B_down_time = time()

def B_released():
    global B_down_time, A_is_held_for_tab

    if diagnostic_mode:
        ledB.off()
        return

    # Debounce
    if B_down_time and time() - B_down_time < DEBOUNCE:
        return

    # TAB combo: A is held, B is tapped
    if A_is_held_for_tab:
        send_tab()
        A_is_held_for_tab = False
        return

    # Normal PAGE DOWN
    page_down()

    B_down_time = None

btnA.when_pressed = A_pressed
btnA.when_released = A_released
btnB.when_pressed = B_pressed
btnB.when_released = B_released

# ------------- Main Loop -----------------

while True:
    now = time()

    # Hold A 5 seconds → toggle diagnostic mode
    if A_down_time and (now - A_down_time) >= 5:
        if not diagnostic_mode:
            enter_diagnostic()
        else:
            exit_diagnostic()

        # Ensure this only triggers once
        A_down_time = None

    sleep(0.02)
