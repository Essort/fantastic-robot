import socketserver
import serial

invertX = True
invertY = True
invertZ = True

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0)


# position calculation
def calcPos(data):

    global ser

    # convert string to array
    dataArr = data.strip(':').split(';')
    print(dataArr)

    # motor controller stepper calculation
    if dataArr[0] != 'x':
        motor1 = 0
        motor2 = 0
        motor3 = 0
        motor4 = 0

        # if we got movement control data, we will process it
        if invertX:
            motor1 = int(dataArr[1]) * -1
            motor2 = int(dataArr[1])
        else:
            motor1 = int(dataArr[1])
            motor2 = int(dataArr[1]) * -1

        if invertY:
            motor3 = int(dataArr[0])
            motor4 = int(dataArr[0]) * -1
        else:
            motor3 = int(dataArr[0]) * -1
            motor4 = int(dataArr[0])

        # roll axis
        if dataArr[2] != "0":
            if invertZ:
                motor1 = motor1 + int(dataArr[2])
                motor2 = motor2 + int(dataArr[2])
                motor3 = motor3 + int(dataArr[2])
                motor4 = motor4 + int(dataArr[2])
            else:
                motor1 = motor1 + int(dataArr[2]) * -1
                motor2 = motor2 + int(dataArr[2]) * -1
                motor3 = motor3 + int(dataArr[2]) * -1
                motor4 = motor4 + int(dataArr[2]) * -1

        # speed controller
        if dataArr[3] != "0":
            if motor1 > 0:
                motor1 = motor1 + int(dataArr[3])
            if motor1 < 0:
                motor1 = motor1 - int(dataArr[3])
            if motor2 > 0:
                motor2 = motor2 + int(dataArr[3])
            if motor2 < 0:
                motor2 = motor2 - int(dataArr[3])
            if motor3 > 0:
                motor3 = motor3 + int(dataArr[3])
            if motor3 < 0:
                motor3 = motor3 - int(dataArr[3])
            if motor4 > 0:
                motor4 = motor4 + int(dataArr[3])
            if motor4 < 0:
                motor4 = motor4 - int(dataArr[3])

        command = str(motor1) + ";" + str(motor2) + ";" + str(motor3) + ";" + str(motor4) + ":"
        print(command)

        # serial data send
        ser.write(bytes(command, 'utf-8'))
        print("serial:" + str(ser.readline()))
        #it's rebooting the arduino
        # ser.close()



######################################################
# TCP socket handler
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))

        # process data
        calcPos(self.data.decode('utf-8'))

        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


if __name__ == "__main__":
    HOST, PORT = "", 27015

    # Create the server, binding to localhost on port 27015
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    try:
        server.serve_forever()

    except KeyboardInterrupt:

        #TODO motor leállítás
        command = "0;0;0;0:"
        server.server_close()

