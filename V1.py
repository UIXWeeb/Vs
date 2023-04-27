import threading

class ChatRoom:
    def __init__(self, name):
        self.name = name
        self.users = []
        self.messages = []

    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user):
        self.users.remove(user)

    def add_message(self, user, message):
        self.messages.append((user, message))

    def display_messages(self):
        for user, message in self.messages:
            print(f"{user}: {message}")

class ChatServer:
    def __init__(self):
        self.rooms = {}

    def create_room(self, name):
        room = ChatRoom(name)
        self.rooms[name] = room

    def join_room(self, room_name, user):
        room = self.rooms[room_name]
        room.add_user(user)

    def leave_room(self, room_name, user):
        room = self.rooms[room_name]
        room.remove_user(user)

    def send_message(self, room_name, user, message):
        room = self.rooms[room_name]
        room.add_message(user, message)

    def display_messages(self, room_name):
        room = self.rooms[room_name]
        room.display_messages()

server = ChatServer()
server.create_room("General")
server.join_room("General", "Alice")
server.send_message("General", "Alice", "Hello everyone!")
server.join_room("General", "Bob")
server.send_message("General", "Bob", "Hi Alice!")
server.display_messages("General")