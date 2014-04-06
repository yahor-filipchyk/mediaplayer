
import sys
import socket
from RequestHandler import RequestHandler

# default hostname and port
HOST = "localhost"
PORT = 8080

def start_server(host=None, port=None):
    if host is None:
        host = HOST
    if port is None:
        port = PORT
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
    except OSError:
        print("Unable to start server on host [{0}] and bind it to port [{1}]. Try to use another hostname or port."
            .format(host, port))
        return
    print("Server is started on host [{0}] and binded to port [{1}].".format(host, port))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        client_connection = RequestHandler(addr, conn)
        client_connection.process_request()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        start_server(host=sys.argv[1])
    elif len(sys.argv) == 3:
        start_server(host=sys.argv[1], port=int(sys.argv[2]))
    else:
        start_server()