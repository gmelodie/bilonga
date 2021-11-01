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


class Bilonga():
    def __init__(self, in_out_ports={80:(8080, default_handler)}):
        self.in_out_ports = in_out_ports

    def run(self):
        for in_port, (out_port, handler) in self.in_out_ports.items():
            threading.Thread(target=self.create_tunnel, args=(in_port, \
                                                              out_port, \
                                                              handler\
                                                              )).start()
            print(f'New tunnel {in_port} -> {handler} -> {out_port}')

    def create_tunnel(self, in_port, out_port, handler_func=default_handler):
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
                threading.Thread(target=process_incomming_connection, \
                                 args=(in_conn, handler_func, out_sock)).start()

    def connection_handler(self, in_port, out_port):
        def decorator(func):
            print(f"New handler: {in_port} -> {func} -> {out_port}")
            if in_port in self.in_out_ports:
                print(f"Handler for port {in_port} overwritten")
            self.in_out_ports[in_port] = (out_port, func)
            return func
        return decorator


if __name__ == '__main__':
    # Bilonga({
        # 85: (86, default_handler),
        # 87:(88, default_handler),
    # }).run()
    Bilonga().run()

