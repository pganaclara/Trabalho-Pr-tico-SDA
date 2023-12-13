import socket
from codecs import decode


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def conectar(self):

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

        print("Aguardando conexão...\n")

        con, address = self.server.accept()
        self.con = con

        return str(address)

    def enviar(self, msg):
        self.con.send(bytes(msg, encoding='UTF-8'))

    def recv(self, size):
        msg = self.con.recv(size)
        return msg.decode()

    def close(self):
        self.con.close()
