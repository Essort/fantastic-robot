import socketserver
import sys

class essortTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        try:
            data = self.data.decode()
            if data != "":
                print("{} wrote:".format(self.client_address[0]))
                print(self.data.decode())
                #example: bin(int.from_bytes(b'\x11', byteorder=sys.byteorder))  # => '0b10001'
                #print(bin(int.from_bytes(self.data, byteorder=sys.byteorder)))

                # now just send back the same data, but upper-cased
                self.request.sendall(self.data.upper())

        except (UnicodeDecodeError, AttributeError):
            pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 18636

    # Create the server, binding to localhost on port 18636
    with socketserver.TCPServer((HOST, PORT), essortTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
