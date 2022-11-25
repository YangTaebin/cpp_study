import socket

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


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect_server(s,(Host,port))
s.sendall(b"Hello, world!\n")
s.close()