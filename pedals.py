#!/usr/bin/python3
from gpiozero import Button
from time import time, sleep
from subprocess import run

btnA = Button(17, pull_up=True, bounce_time=0.3)
btnB = Button(27, pull_up=True, bounce_time=0.3)

last_event_time = 0
DEBOUNCE_TOTAL = 0.25   # Total debounce window in seconds

def keypress(k):
    print("Sending:", k)
    run(["wtype", "-k", k])

def A_released():
    global last_event_time
    now = time()
    if now - last_event_time < DEBOUNCE_TOTAL:
        return
    last_event_time = now
    keypress("Down")

def B_released():
    global last_event_time
    now = time()
    if now - last_event_time < DEBOUNCE_TOTAL:
        return
    last_event_time = now
    keypress("Up")

btnA.when_released = A_released
btnB.when_released = B_released

print("Stable test mode running… A=Down, B=Up")

while True:
    sleep(0.01)
