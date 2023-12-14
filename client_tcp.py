import socket
import threading

# Request do Servidor
message = ""

# Função executada em uma thread para plotar os dados do gráfico


def client_tcp():

    global message

    # Configurações do servidor
    host = 'localhost'  # Endereço IP do servidor
    port = 51510  # Porta do servidor

    # Criação do socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Conecta ao servidor
    client_socket.connect((host, port))

    while True:
        message = input("Sinal de controle (0~10)")

        # Envio de dados para o servidor
        client_socket.send(message.encode('utf-8'))
        print("Sinal de controle enviado: " + message)
        # Recebe a resposta do servidor
        response = client_socket.recv(1024).decode('utf-8')

        # Comando kill mata o cliente
        if response == "kill":
            # Encerra a conexão com o servidor

            client_socket.close()
            break
        else:
            print("Velocidade do motor: " + response)


def main():
    global hyst
    global message

    graph_thread = threading.Thread(target=client_tcp)
    graph_thread.start()


if __name__ == "__main__":
    main()
