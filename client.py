import socket


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def conectar(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.host, self.port))

    def recv(self, size):
        msg = self.server.recv(1024)
        return msg

    def enviar(self, msg):
        self.server.send(bytes(msg, encoding='UTF-8'))

    def close(self):
        self.server.close()
