import socket
import threading

def process_incomming_connection(connection, out_sock):
    with connection:
        data = connection.recv(1024)
        while data:
            out_sock.sendall(data)
            data = connection.recv(1024)


def create_tunnel(in_port, out_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as in_sock, \
            socket.socket(socket.AF_INET, socket.SOCK_STREAM) as out_sock:

        out_sock.connect(('localhost', out_port))
        print(f"Connected to out_port {out_port}")
        in_sock.bind(('0.0.0.0', in_port))
        in_sock.listen()
        print(f"Accepting connections on in_port {in_port}")
        while True:
            in_conn, in_addr = in_sock.accept()
            print(f"Incomming connection from {in_addr}")
            threading.Thread(target=process_incomming_connection, args=(in_conn, out_sock)).start()


def bilonga(in_port=80, out_port=8080):
    while True:
        create_tunnel(in_port, out_port)
        print(f'New tunnel {in_port} -> {out_port}')


if __name__ == '__main__':
    bilonga(in_port=82, out_port=8082)

