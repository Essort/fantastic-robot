# fantastic-robot
This is the repository of the Obelisk 2 robot. (github suggested the name :) )

# OAK-D camera mount
This is the 3D printable OAK-D mount used on our robot (it can be downloaded here too: https://www.tinkercad.com/things/eBv3UJN90H8 )


#Python programs

## Example directory - (test programs)

### socketServer.py<br>
For host testing. Simple echo server

### socketClient.py<br>
Simple client for sending one message, and receive response

### socketListener.py<br>
Continous listening for messages from the server.

### remoteController.py<br>
For joystick control for example: logitech Extreme 3D Pro

### remoteController_xbox360.py<br>
For xbox 360 controller

### robotController.py<br>
Main python program running on the robot. The head, and stepper motor controller
- This requires adafruit-circuitpython-servokit 
- run on rpi:
  ```
  python -m pip install -r requirements.txt
  python -m pip install -r requirements_rpi.txt
  ```

### robotController_only_move.py<brr>
Test program for only to move the robot
- it can be used to test the communication on windows

---
## Pre-requisites

1. create virtualenv enviroment

2. Install requirements
   ```
   python -m pip install -r requirements.txt
   ```

---
## RPi PWM shield

from this guide: https://www.waveshare.com/wiki/Servo_Driver_HAT

1. Enable I2C Interface

```
sudo raspi-config 
Choose Interfacing Options -> I2C ->yes 
sudo reboot
```

2. Install libraries

```
python -m pip install -r requirements_rpi.txt
```

  
 # coming  soon:
- Arduino source code
- custom PCB shield for the arduino
- Unreal Engine 4 project with the stereo camera, and OAK-D support
