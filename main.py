import time
import os.path
from threading import *
from client import Client
from datetime import datetime

# Motores em funcionamento
id_motores = []

# Criando objetos semaforo
sem_obj = Semaphore(4)

# Modo de funcionamento
remote_mode = bool(True)

# Globais
km = 2.25
kb = 2
ra = 3
la = 4
T = 1
b = 1
jm = 5
voltage = 2
speed = 0
torque = 0
speed_reference = 0
msg = ""
num_motores = 10

# Criando a comunicação
if remote_mode:
    client = Client("127.0.0.1", 51511)
    client.conectar()

# Thread  interface


def interface_thread():
    global speed_reference

    if remote_mode:
        a = client.recv(8024)
        if a != "-":
            speed_reference = int(a)
    else:
        speed_reference = input("\nQual velocidade de referência: ")
        speed_reference = int(speed_reference)

    wait_ref.set()
    wait_ref.clear()


def recebeVelocidade(sc):
    global speed
    return speed


# Thread logger


def logger_thread():
    global msg

    while (1):
        if (os.path.isfile("log.txt")):
            file = open("log.txt", 'a')
        else:
            file = open("log.txt", "x")

        dt = datetime.now()
        ts = datetime.timestamp(dt)

        msg = "\n" + "Time stamp: " + \
            str(ts) + " Date time: " + str(dt) + "\n \n"

        for i in range(num_motores):
            if i in id_motores:
                msg += "Motor " + str(i+1) + \
                    " | Velocidade: " + str(speed) + "\n"
            else:
                msg += "Motor " + str(i+1) + " | Velocidade: 0" + "\n"

        file.write(str(msg))
        time.sleep(5)


# Thread dos motores
def motor_thread(id):
    global speed, torque

    # Adquiriu posse
    sem_obj.acquire()

    verify_sequence.acquire()

    # Verificar se existe motor em sequência ativo
    if id+1 in id_motores or id-1 in id_motores or id in id_motores:
        sem_obj.release()
        verify_sequence.release()

    else:
        id_motores.append(id)
        verify_sequence.release()
        start_time = time.time()
        t = start_time

        while (t < start_time + 10):
            t = time.time()
            print(t, speed, id)
            motor_timer.wait()
            torque = (T*(km*voltage - km*kb*speed - ra*torque))/la + torque
            speed = (T*(torque - b*speed))/jm + speed
            print("Motor de índice ", id+1, " com velocidade de: ", speed)
            msgMotor = "Motor de índice ", id+1, " com velocidade de: ", speed
            client.enviar(str(msgMotor))

        id_motores.remove(id)
        sem_obj.release()


# Thread de controle
def control_thread():
    global voltage
    result = 0

    while (1):
        control_timer.wait()
        result += T*(speed_reference-speed)
        voltage = result + speed_reference - speed


# Temporizadores
def timers():

    while (1):
        i = Thread(target=interface_thread, daemon=True)
        i.start()
        if remote_mode:
            client.enviar(msg)
        wait_ref.wait()

        start_time = time.time()
        t = start_time

        # Esperando pelo fim da simulação
        while (t < start_time + 10):
            t = time.time()

            # Permite a simulação do motor_thread
            # dentro do perído de 100ms
            motor_timer.set()
            motor_timer.clear()
            time.sleep(0.1)

            # Permite a simulação do control_thread
            # dentro do perído de 200ms
            control_timer.set()
            control_timer.clear()
            time.sleep(0.2)


# Iniciando a thread
if __name__ == "__main__":

    wait_ref = Event()

    # Mutex para acesso a variáveis globais
    verify_sequence = Lock()

    # Timer usados para definir frequencia de cada thread
    motor_timer = Event()
    control_timer = Event()

    # Criando thread do controle e timer
    c = Thread(target=control_thread, daemon=True)
    t = Thread(target=timers, daemon=True)
    l = Thread(target=logger_thread, daemon=True)

    # Iniciando threads
    c.start()
    t.start()
    l.start()

    # Vetor para armazenar as threads
    threads = []

    # Criando thread motores
    while (1):
        for i in range(num_motores):
            m = Thread(target=motor_thread, args=(i, ))
            m.start()
            threads.append(m)

    # Finalizando
    threads.append(i)
    threads.append(c)
    threads.append(t)
    threads.append(l)

    for i in threads:
        i.join()
