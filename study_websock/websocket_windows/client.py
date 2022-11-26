import socket
import threading

Host = "43.201.73.94"
port = 8000

def connect_server(socket, address):
    connection_trial = 10
    for i in range(connection_trial):
        try:
            socket.connect(address)
            print("\rconnection success")
            break
        except:
            print(f"\rconnection failed... | trial: {i + 1}/{connection_trial}", end="")


def send_hw_serv():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect_server(s,(Host,port))
    s.sendall(b"Hello, world!\n")
    s.close()

t1 = threading.Thread(target=send_hw_serv)
t2 = threading.Thread(target=send_hw_serv)
t3 = threading.Thread(target=send_hw_serv)
t4 = threading.Thread(target=send_hw_serv)
t5 = threading.Thread(target=send_hw_serv)
t6 = threading.Thread(target=send_hw_serv)
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()