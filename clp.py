import socket
import time
from opcua import Client
from motores import recebeVelocidade
from motores import setSpeed
from server import Server


def client_opc(sc):

    server = Server("127.0.0.1", 51511)
    address = server.conectar()

    print("Conectado no endereço: ", address)

    server.enviar("2")

    start_time = time.time()
    t = start_time

    msg = server.recv(8024)
    print(msg)
    while (t < start_time + 10):
        msg = server.recv(8024)
        print(msg)
        server.enviar("-")

        if not msg:
            print("\n connection terminated")
            server.close()
            break

    server.close()

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

    # Retorna a velocidade do motor


def main():
    client_opc(1)
    # # Configurações do servidor
    # host = 'localhost'  # Endereço IP do servidor
    # port = 51510  # Porta a ser usada pelo servidor

    # # Criação do socket
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # # Vincula o socket ao endereço e porta
    # server_socket.bind((host, port))

    # # Coloca o socket em modo de escuta
    # server_socket.listen(1)

    # print('Aguardando conexões...')
    # # Aguarda uma conexão do cliente
    # client_socket, client_address = server_socket.accept()
    # print('Conexão estabelecida com', client_address)

    # while True:
    #     # Recebe dados enviados pelo cliente
    #     data = client_socket.recv(1024).decode('utf-8')

    #     # Encerra a conexão
    #     if data == "kill":
    #         client_socket.send("kill".encode('utf-8'))
    #         print("Comando de encerramento de conexão enviado")
    #         break
    #     else:
    #         print("Sinal de controle recebido: " + data)

    #     data = float(data)
    #     response = client_opc(data)
    #     response = str(round(response, 3))

    #     start_time = time.time()
    #     t = start_time

    #     while (t < start_time + 10):
    #         # Envia a resposta de volta para o cliente
    #         data = float(data)
    #         response = client_opc(data)
    #         response = str(round(response, 3))
    #         client_socket.send(response.encode('utf-8'))
    #         print("Nível enviado: " + response + "\n")

    #     # Loop pra ir vendo a velocdiade

    # # Encerra a conexão com o cliente
    # client_socket.close()


if __name__ == "__main__":
    main()
