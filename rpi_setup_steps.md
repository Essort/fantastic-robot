# Setup of the RPI

 1. Create SD card with raspbian lite image
 2. sudo apt-get update
 3. sudo apt-get upgrade
 4. sudo apt-get install git
 5. git clone --depth=1 https://github.com/pikvm/ustreamer
 6. cd ustreamer/
 7. sudo apt install libevent-dev libjpeg8-dev libbsd-dev libraspberrypi-d
 8. make WITH_OMX=1

# check camera

    v4l2-ctl --list-devices
    v4l2-ctl -d /dev/video0 --list-formats-ext
    v4l2-ctl -d /dev/video2 --list-formats-ext

    ./ustreamer --device=/dev/video0 --format=MJPEG --host=192.168.0.15 -p 8080 -r 1280x720
    ./ustreamer --device=/dev/video2 --format=MJPEG --host=192.168.0.15 -p 8081 -r 1280x720

# setup camera auto start script

 1. sudo apt-get install screen
 2. start script:  "startLeftCamScreen" (and one for the other camera: startRightCamScreen)
the --host have to be the device IP !
```
# startLeftCamScreen
cd ~/ustreamer && ./ustreamer --device=/dev/video0 --format=MJPEG --host=192.168.0.16 -p 8080 -r 1280x720 --allow-origin *
```
```
# startRightCamScreen
cd ~/ustreamer && ./ustreamer --device=/dev/video1 --format=MJPEG --host=192.168.0.16 -p 8081 -r 1280x720 --allow-origin *
```

Set to executable
```
chmod +x ~/startLeftCamScreen
chmod +x ~/startRightCamScreen
```

Edit the root startup script file

```
sudo nano /etc/rc.local
```

And the following line before `exit  0`

```
# Run a command as `pi` from the home folder 
# in a screen named `pistartup`
su - pi -c "screen -dm -S leftCam ~/startLeftCamScreen"
su - pi -c "screen -dm -S rightCam ~/startRightCamScreen"
```

# helpfull commands
```
#check for running screens
screen -list

#ressume screen
screen -r <screen_id>
```

# notes
At VR (PC) side, you have to make a simple html for embed mjpeg stream (example in the repo) because currently webBrowser UE widget can't open the stream directly.
//with the simple HTML you can configure the position screen size etc. with the html for the VR

