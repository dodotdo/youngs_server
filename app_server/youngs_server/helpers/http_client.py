import asyncore
import socket

class HTTPClient(asyncore.dispatcher):
    def __init__(self, host, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, 8000))

    def handle_connect(self):
        print('socket connected')
        pass

    def handle_close(self):
        print('socket closed')
        self.close()

    def handle_read(self):
        print(self.recv(100))

    def writable(self):
        return ''

    def handle_write(self):
        sent = self.send(self.bufferr)
        self.buffer = self.buffer[sent:]
