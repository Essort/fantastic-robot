import pygame

# for debug
import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen [width,height]
size = [350, 400]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Essort Robot Controller")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Get ready to print
textPrint = TextPrint()

# previous command
prevCommand = ""

#max speed
maxSpeed = 300

#############################################################
# socket send
def sendSocketComm(data):
    import socket
    import sys

    ##Robot IP adddress defined here
    HOST, PORT = "192.168.2.103", 27015


    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(data.encode())

        # Receive data from the server and shut down
        received = sock.recv(1024).decode()
    finally:
        sock.close()

    print("Sent:     {}".format(data))
    print("Received: {}".format(received))

    return


###############################################################
# -------- Main Program Loop -----------
while done == False:

    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")

    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        # for i in range(joystick_count-1):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.print(screen, "Joystick {}".format(i))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes))
        textPrint.indent()

        data = "";
        for i in range(axes):
            axis = joystick.get_axis(i)
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis))
            # speed control calculated differently
            if (data != ""):
                data += ";"
            if (i == 4):
                # xbox 360 - right analog stick foward, backward
                # 0-200 speed controller
                # data += str(round(((axis * -100) + 100)))
                # 0-100 speed controller
                # data += str(round(((axis * -50) + 50)))
                # configurable
                data += str(round(((axis * - (maxSpeed / 4)) + (maxSpeed / 4))))
            else:
                if i == 0 or i == 1:
                    if (abs(axis * 100) > 15):
                        # -100 <> +100 X-Y axis //-50 <> +50 X-Y axis slow speed
                        # default speed
                        # data += str(round((axis * 100)))
                        #
                        # configurable
                        data += str(round((axis * maxSpeed)))

                else:
                    # deadzone, under 15 we don't send data
                    data += "0"
        textPrint.unindent()

        if (str(joystick.get_button(8)) == "1"):
            data += ";1"
        else:
            data += ";0"

        data += ";" + str(joystick.get_button(4))  # fel
        data += ";" + str(joystick.get_button(2))  # le
        data += ":";

        if (prevCommand != data):
            prevCommand = data
            sendSocketComm(data)
            print(data)

        buttons = joystick.get_numbuttons()
        textPrint.print(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()

        for i in range(buttons):
            button = joystick.get_button(i)
            textPrint.print(screen, "Button {:>2} value: {}".format(i, button))
        textPrint.unindent()

        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)

# socket close
# sock.close()

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

