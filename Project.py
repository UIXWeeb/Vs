import socket
import threading

class ChatServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', 12345))
        self.server_socket.listen(5)
        self.clients = []

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f'New connection from {client_address}')
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f'Received message: {message}')
                for client in self.clients:
                    if client != client_socket:
                        client.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f'Error: {e}')
                break
        print('Closing connection')
        self.clients.remove(client_socket)
        client_socket.close()

if __name__ == '__main__':
    server = ChatServer()
    server.start()
