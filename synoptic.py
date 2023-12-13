import os.path
import multiprocessing
from server import Server


def synoptic_process():

    server = Server("127.0.0.1", 51511)
    address = server.conectar()

    print("Conectado no endereço: ", address)

    speed_reference = input("\nQual velocidade de referência: ")
    server.enviar(speed_reference)

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

        speed_reference = input("\nQual velocidade de referência: ")
        server.enviar(speed_reference)


if __name__ == "__main__":
    synoptic = multiprocessing.Process(target=synoptic_process())
