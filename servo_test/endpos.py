import time
import threading
import socketserver
from PCA9685 import PCA9685
from time import ctime

import termios, sys, tty

print("start")

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

Pos0 = 1500
Pos1 = 2000
Pos2 = 1500
Step0 = 0
Step1 = 0
Step2 = 0
pwm.setServoPulse(0, Pos0)
pwm.setServoPulse(1, Pos1)
pwm.setServoPulse(2, Pos2)

time.sleep(5)

servo0Max = 2100
servo0Min = 1000

servoMax = 2000
servoMin = 1500


def _getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)  # This number represents the length
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def examples():
    global Step0, Step1, Step2, Step3

    while True:

        data = _getch()
        # print(data)

        if not data:
            break
        if data == " ":
            Step0 = 0
            Step1 = 0
            Step2 = 0
        elif data == "a":
            Step0 = -5
            print(str(servo0Min))
        elif data == "d":
            Step0 = 5
            print(str(servo0Max))
        elif data == "r":
            Step1 = -5
            print(str(servoMin))
        elif data == "f":
            Step1 = 5
            print(str(servoMax))
        elif data == "g":
            Step2 = -5
            print(str(servoMin))
        elif data == "t":
            Step2 = 5
            print(str(servoMax))
        elif data == "q":
            sys.exit()


def timerfunc():
    global Step0, Step1, Step2, Step3, Pos0, Pos1, Pos2, Pos3, pwm

    # balra jobbra
    if (Step0 != 0):
        Pos0 += Step0
        if (Pos0 >= servo0Max):
            Pos0 = servo0Max
        if (Pos0 <= servo0Min):
            Pos0 = servo0Min
        # set channel 0
        pwm.setServoPulse(0, Pos0)

    if (Step1 != 0):
        Pos1 += Step1
        if (Pos1 >= servoMax):
            Pos1 = servoMax
        if (Pos1 <= servoMin):
            Pos1 = servoMin
        # set channel 1
        pwm.setServoPulse(1, Pos1)

    if (Step2 != 0):
        Pos2 += Step2
        if (Pos2 >= servoMax):
            Pos2 = servoMax
        if (Pos2 <= servoMin):
            Pos2 = servoMin
        # set channel 2
        pwm.setServoPulse(2, Pos2)

    global t  # Notice: use global variable!
    t = threading.Timer(0.02, timerfunc)
    t.start()


t = threading.Timer(0.02, timerfunc)
t.setDaemon(True)
t.start()

examples()
