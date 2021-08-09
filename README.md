Project build log:
https://hackaday.io/project/167713

#Python programs

### main.py<br>
This is the main program, with object detection. It can detect and distinguishes objects.
It contains a TCP server. When client connected this will post a JSON array to a client.
The array contains, camera ID, detected object name, x, y coordinates, and Z for the depth (distance to the detected object)
When we are testing it we used with multiple instances with different camera ID, because we don't need frame synced operation.

## Example directory - (test programs)

### 1_example_depthai.py<br>
This is used to exporting images with various colormaps for testing

### 2_example_depth_tcp.py<br>
This is the TCP server to test the depth map visualisation in unreal engine

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
  python -m pip install -r requirements_v2.txt
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

## models directory
It contains the model for the main.py (object detection)




