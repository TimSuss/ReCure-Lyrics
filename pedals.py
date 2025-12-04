#!/usr/bin/python3
from gpiozero import Button
from subprocess import run
from time import sleep

btnA = Button(17, pull_up=True)
btnB = Button(27, pull_up=True)

def keypress(key):
    print("Sending:", key)
    run(["wtype", "-k", key])

def A_released():
    keypress("Down")

def B_released():
    keypress("Up")

btnA.when_released = A_released
btnB.when_released = B_released

print("RUNNING SIMPLE TEST MODE")
print("A = Down  |  B = Up")

while True:
    sleep(0.05)
