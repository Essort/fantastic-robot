import time
from PCA9685 import PCA9685

print("start")

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

# servo 0 left - right
servo0Max = 2100
servo0Min = 700

# 1830 center level
center = 1830
full_up = -300
full_down = 130

while True:

    input_val = input()
    print("input 1: ", input_val)

    #pwm.setServoPulse(1, center + int(input_val))
    #pwm.setServoPulse(2, center - int(input_val))

    pwm.setServoPulse(1, center + int(input_val))
    pwm.setServoPulse(2, center + int(input_val))
