import socketserver
# import termios, sys, tty
from PCA9685 import PCA9685

# initialise pwm shield
pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

# head movement servo default offset value (90 center)
servo0 = 1400  # SERVO1 - PAN/YAW - Z
servo1 = 1830  # SERVO2 - ROLL and TILT/PITCH (X,Y)
servo2 = 1830  # SERVO3 - ROLL and TILT/PITCH (X,Y)

# TODO calibrate full 180 length now it's only 90..
# Z HTC - PAN/YAW -> 0 180 -- 90 -- HW LIMIT 1000-2000 HW center: 1500
servo0Max = 2100  # left
servo0Min = 700  # right
servo0Distance = 700

# X HTC - ROLL
# Y HTC - TILT/PITCH
servo1Min = 1500  # servo1:1500 and servo2:2000 full up
servo1Max = 2000  # servo1:2000 and servo2:1500 full down
servo1UpRange = -300
servo1DownRange = 130


# check if limit reached PAN
def check_pwm_pan(pwm_value):
    if servo0Min <= pwm_value <= servo0Max:
        return True
    else:
        return False


# check if limit reached TILT
def check_pwm_tilt(pwm_value):
    if servo1Min <= pwm_value <= servo1Max:
        return True
    else:
        return False


# send data to PWM shield
def set_servo_pos(s5, s6, s7):
    if check_pwm_pan(s5):
        print("s5:", s5)
        # pwm.setPWM(4, 0, s5)
        pwm.setServoPulse(0, s5)
    if check_pwm_tilt(s6):
        print("s6:", s6)
        # pwm.setPWM(6, 0, s6)
        pwm.setServoPulse(1, s6)
    if check_pwm_tilt(s7):
        print("s7:", s7)
        # pwm.setPWM(5, 0, s7)
        pwm.setServoPulse(2, s7)


# recalculate PWM for head position
def remap_in_range(val, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    if old_range == 0:
        new_val = new_min
    else:
        new_range = (new_max - new_min)
        new_val = (((val - old_min) * new_range) / old_range) + new_min

    return round(new_val)


# position calculation
def calc_pos(data):
    # convert string to array
    data_arr = data.strip(';').split(':')
    print(data_arr)

    # TODO motor controller stepper calculation
    if data_arr[0] != 'x':
        # if we got movement control data, we will process it
        print("TODO")

    # head movement calculation
    if data_arr[4] != 'x':

        # if we got head position data, we will process it
        j4 = int(data_arr[4])  # ROLL
        j5 = int(data_arr[5])  # PITCH/TILT
        j6 = int(data_arr[6])  # YAW/PAN - left + right

        # max or min
        if j4 < servo1UpRange:
            j4 = servo1UpRange
        if j4 > servo1DownRange:
            j4 = servo1DownRange

        if j5 < servo1UpRange:
            j5 = servo1UpRange
        if j5 > servo1DownRange:
            j5 = servo1DownRange

        if j6 < servo0Distance * -1:
            j6 = servo0Distance * -1
        if j6 > servo0Distance:
            j6 = servo0Distance

        # PITCH / TILT
        s6 = s7 = 0
        if servo1UpRange <= j5 <= servo1DownRange:
            s6 = remap_in_range(j5, servo1UpRange, servo1DownRange, servo1Max, servo1Min)
            s7 = remap_in_range(j5, servo1UpRange, servo1DownRange, servo1Min, servo1Max)

        # ROLL
        # if servo1UpRange <= j4 <= servo1DownRange:
        if -300 <= j4 < 0:
            roll = j4
            s6 += roll
            s7 += roll / 2
        elif 0 < j4 <= 300:
            roll = j4
            s6 += roll * 2
            s7 += roll

        # servoPan
        s5 = 0
        if servo0Distance * -1 <= j6 <= servo0Distance:
            s5 = remap_in_range(j6, servo0Distance * -1, servo0Distance, servo0Max, servo0Min)

        # send PWM data to the PWM shield
        set_servo_pos(s5, s6, s7)

    # TODO - we need this?
    # time.sleep(0.005)


######################################################
# TCP socket handler
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        try:
            data = self.data.decode()
            if data != "":
                print("{} wrote:".format(self.client_address[0]))
                print(self.data.decode())

                # process data
                calc_pos(self.data.decode('utf-8'))

                # just send back the same data, but upper-cased
                self.request.sendall(self.data.upper())

        except (UnicodeDecodeError, AttributeError):
            pass


if __name__ == "__main__":
    HOST, PORT = "", 27015

    socketserver.TCPServer.allow_reuse_address = True

    # Create the server, binding to localhost on port 27015
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:

        set_servo_pos(servo0, servo1, servo2)

        server.serve_forever()

    except KeyboardInterrupt:

        server.server_close()
