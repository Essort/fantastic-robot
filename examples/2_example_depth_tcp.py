#!/usr/bin/env python3

import cv2
import depthai as dai
import socketserver
import threading
from time import sleep


# TCP server
class TCPServerRequest(socketserver.BaseRequestHandler):
    def handle(self):
        # Handle is called each time a client is connected
        while True:
            sleep(0.1)
            if hasattr(self.server, 'datatosend'):
                # self.request.send(self.server.datatosend.encode() + "\r\n".encode())

                try:
                    data = self.server.datatosend
                    if data != "":
                        print("sent to {}".format(self.client_address[0]))
                        # print(self.server.datatosend)

                        # just send
                        # self.request.sendall(self.server.datatosend.encode())
                        #rList = [1, 2, 3, 4, 5]
                        #self.request.sendall(bytearray(rList))
                        self.request.sendall(self.server.frametosend)

                except (UnicodeDecodeError, AttributeError):
                    pass

                # to stop resend
                self.server.datatosend = ""


# start TCP data server
socketserver.TCPServer.allow_reuse_address = True
server_TCP = socketserver.TCPServer(('localhost', 18636), TCPServerRequest)
server_TCP.datatosend = "hello"
th = threading.Thread(target=server_TCP.serve_forever)
th.daemon = True
th.start()

# Start defining a pipeline
pipeline = dai.Pipeline()

# Define a source - two mono (grayscale) cameras
left = pipeline.createMonoCamera()
left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
left.setBoardSocket(dai.CameraBoardSocket.LEFT)

right = pipeline.createMonoCamera()
right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)  # 640×400
right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
depth = pipeline.createStereoDepth()

# original - default 200
depth.setConfidenceThreshold(200)

# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
median = dai.StereoDepthProperties.MedianFilter.KERNEL_7x7  # For depth filtering
depth.setMedianFilter(median)

'''
If one or more of the additional depth modes (lrcheck, extended, subpixel)
are enabled, then:
 - depth output is FP16. TODO enable U16.
 - median filtering is disabled on device. TODO enable.
 - with subpixel, either depth or disparity has valid data.
Otherwise, depth output is U16 (mm) and median is functional.
But like on Gen1, either depth or disparity has valid data. TODO enable both.
'''
# Better handling for occlusions:
depth.setLeftRightCheck(False)
# Closer-in minimum depth, disparity range is doubled:
depth.setExtendedDisparity(False)
# Better accuracy for longer distance, fractional disparity 32-levels:
depth.setSubpixel(False)

left.out.link(depth.left)
right.out.link(depth.right)

# Create output
xout = pipeline.createXLinkOut()
xout.setStreamName("disparity")
depth.disparity.link(xout.input)

colormap = cv2.COLORMAP_JET

# Pipeline is defined, now we can connect to the device
with dai.Device(pipeline) as device:
    # Start pipeline
    device.startPipeline()

    # Output queue will be used to get the disparity frames from the outputs defined above
    q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)

    while True:
        inDepth = q.get()  # blocking call, will wait until a new data has arrived
        frame = inDepth.getFrame()
        # options: NORM_L1 NORM_L2 NORM_INF this working: NORM_MINMAX
        frame = cv2.normalize(frame, None, 0, 255, cv2.NORM_MINMAX)

        cv2.imshow("raw", frame)
        rawFrame = frame

        # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
        # frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
        frame = cv2.applyColorMap(frame, colormap)

        # frame is ready to be shown
        cv2.imshow("disparity", frame)

        # store image
        # cv2.imwrite("export/frame_" + str(colormap) + ".jpg", frame)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
			
		# colormap test for unreal engine demo
        elif key == ord('n'):
            if colormap < 21:
                colormap = colormap + 1
        elif key == ord('p'):
            if colormap > 0:
                colormap = colormap - 1
		
		# sending data to unreal engine
        if server_TCP.datatosend == "":
            list = []

            resized = cv2.resize(rawFrame, (320, 200))

            cv2.imshow("resized", resized)

            if server_TCP.datatosend == "":
                print(resized[10][10])
                for x in range(len(resized)):
                    for y in range(len(resized[x])):
                        #print(rawFrame[x][y])
                        #data = data + ":" + str(rawFrame[x][y])
                        list.append(resized[x][y])

                server_TCP.frametosend = bytearray(list)
                #print(server_TCP.frametosend)
                server_TCP.datatosend = "ok"
            # https://www.geeksforgeeks.org/python-bytearray-function/
            # https://stackoverflow.com/questions/48988266/convert-python-byte-array-to-int-array
            #server_TCP.datatosend = bytearray(rawFrame)


