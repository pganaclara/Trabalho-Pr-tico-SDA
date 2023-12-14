import socket
import time
import os.path
from opcua import Client
from server import Server


def client_opc(data):

    server = Server("127.0.0.1", 51511)
    address = server.conectar()

    print("Conectado no endereço: ", address)

    speed_reference = input("\nQual velocidade de referência: ")
    server.enviar(str(data))

    while True:
        msg = server.recv(8024)
        print(msg)

        if not msg:
            print("\n connection terminated")
            server.close()
            break
        else:

            if (os.path.isfile("historiador.txt")):
                file = open("historiador.txt", 'a')
            else:
                file = open("historiador.txt", "x")

            file.write(str(msg))

        return msg

    # Resta tratar a string msg para inserir seus valores nos nodes
    
    # # cria o client
    # client = Client("opc.tcp://DESKTOP-HGTMO6N:53530/OPCUA/SimulationServer")

    # client.connect()

    # node_velocidade_motor = client.get_node(
    #     "ns=3;i=1009")  # node da velocidade do motor

    # # recebe a velocidade do motor
    # velocidade = recebeVelocidade(sc)

    # # escreve valor da velocidade do motor no OPC
    # node_velocidade_motor.set_value(velocidade)

    # client.disconnect()


def main():
    # Configurações do servidor
    host = 'localhost'  # Endereço IP do servidor
    port = 51510  # Porta a ser usada pelo servidor

    # Criação do socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Vincula o socket ao endereço e porta
    server_socket.bind((host, port))

    # Coloca o socket em modo de escuta
    server_socket.listen(1)

    print('Aguardando conexões...')
    # Aguarda uma conexão do cliente
    client_socket, client_address = server_socket.accept()
    print('Conexão estabelecida com', client_address)

    while True:
        # Recebe dados enviados pelo cliente
        data = client_socket.recv(1024).decode('utf-8')

        # Encerra a conexão
        if data == "kill":
            client_socket.send("kill".encode('utf-8'))
            print("Comando de encerramento de conexão enviado")
            break
        else:
            print("Sinal de controle recebido: " + data)

        data = int(data)
        response = client_opc(data)

        # Envia a resposta de volta para o cliente
        client_socket.send(response.encode('utf-8'))
        print("Nível enviado: " + response + "\n")

    # Encerra a conexão com o cliente
    client_socket.close()


if __name__ == "__main__":
    main()
