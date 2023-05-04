import socket
import threading

# Set up socket connection
host = 'localhost'
port = 55555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Store chat rooms
chat_rooms = {'room1': [], 'room2': []}

# Define function for handling client connections
def handle_client(conn, addr):
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message.startswith('/join'):
                # Join a chat room
                room_name = message.split()[1]
                chat_rooms[room_name].append(conn)
                conn.send(f'Joined {room_name} chat room\n'.encode('utf-8'))
            elif message.startswith('/list'):
                # List available chat rooms
                rooms = list(chat_rooms.keys())
                conn.send(f'Available chat rooms: {", ".join(rooms)}\n'.encode('utf-8'))
            elif message.startswith('/quit'):
                # Quit chat room
                for room_name, connections in chat_rooms.items():
                    if conn in connections:
                        connections.remove(conn)
                        conn.send(f'Left {room_name} chat room\n'.encode('utf-8'))
            else:
                # Send message to all clients in chat room
                for connections in chat_rooms.values():
                    if conn in connections:
                        for connection in connections:
                            if connection != conn:
                                connection.send(message.encode('utf-8'))
        except:
            # Remove client from all chat rooms and close connection
            for connections in chat_rooms.values():
                if conn in connections:
                    connections.remove(conn)
            conn.close()
            break

# Start accepting client connections
print(f'Server listening on {host}:{port}')
while True:
    conn, addr = server.accept()
    print(f'Connected by {addr}')
    threading.Thread(target=handle_client, args=(conn, addr)).start()
