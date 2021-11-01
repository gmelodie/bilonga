import socket
import threading

def default_handler(data):
    return data

def process_incomming_connection(connection, handler_func, out_sock):
    with connection:
        data = connection.recv(1024)
        while data:
            out_sock.sendall(handler_func(data.decode()).encode())
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
            # TODO: change default_handler to decorator
            threading.Thread(target=process_incomming_connection, args=(in_conn, default_handler, out_sock)).start()

def bilonga(in_out_ports=[(80,8080)]):
    for in_port, out_port in in_out_ports:
        threading.Thread(target=create_tunnel, args=(in_port, out_port)).start()
        print(f'New tunnel {in_port} -> {out_port}')

if __name__ == '__main__':
    bilonga([(85,86), (87, 88)])

