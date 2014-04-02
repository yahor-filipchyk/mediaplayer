
import socket
from client_communication import ServerThread

HOST = "localhost"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(10)

while True:
    conn, addr = server.accept()
    thread = ServerThread(addr, conn)
    thread.process_request()
