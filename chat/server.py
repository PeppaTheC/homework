import socket as sock
import select

IP = ''
PORT = 9000
HEADER_LENGTH = 10

server_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
server_socket.setsockopt(sock.SOL_SOCKET, sock.SO_REUSEADDR, True)

server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}
username = {}
name_counter = 0


def receive_data(client_socket: sock.socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return client_socket.recv(message_length)
    except (ValueError, sock.error,):
        return False


def receive_user_message(client_socket: sock.socket):
    _ = receive_data(client_socket)
    whom = receive_data(client_socket)
    message = receive_data(client_socket)
    if whom and message:
        return {'whom': whom, 'message': message}
    return False


def get_header(text: bytes) -> bytes:
    return f"{len(text):<{HEADER_LENGTH}}".encode('utf-8')


def receive_user_name(client_socket: sock.socket):
    return receive_data(client_socket)


def send_users_online(socket: sock.socket):
    for client_socket in clients:
        if client_socket != socket:
            send_user_connection(socket, clients[client_socket], True)
            send_user_connection(client_socket, clients[socket], True)


def send_users_disconnect(socket: sock.socket):
    for client_socket in clients:
        if client_socket != socket:
            send_user_connection(client_socket, clients[socket], False)


def send_user_connection(client_socket: sock.socket, online_user: str, status: bool):
    command = '1' if status else '2'
    from_who = 'host'
    message = online_user
    send_message(from_who, command, message, client_socket)


def send_message(from_who: str, whom: str, message: str, client_socket: sock.socket):
    from_who = from_who.encode('utf-8')
    from_who_header = get_header(from_who)
    whom = whom.encode('utf-8')
    whom_header = get_header(whom)
    message = message.encode('utf-8')
    message_header = get_header(message)
    client_socket.send(from_who_header + from_who + whom_header + whom + message_header + message)


def send_name(client_socket: sock.socket, name: str):
    name = name.encode('utf-8')
    name_header = get_header(name)
    client_socket.send(name_header + name)


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for socket in read_sockets:

        if socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_user_name(client_socket).decode('utf-8')
            if user is False:
                continue
            if user in username:
                user += str(name_counter)
                name_counter += 1
            send_name(client_socket, user)
            sockets_list.append(client_socket)
            clients[client_socket] = user
            username[user] = client_socket

            send_users_online(client_socket)
            print(f"Accepted new connection {client_address[0]}:{client_address[1]} "
                  f"username: {user}")
        else:
            message = receive_user_message(socket)

            if message is False:
                print(f"Closed connection from {clients[socket]}")
                send_users_disconnect(socket)
                sockets_list.remove(socket)
                del username[clients[socket]]
                del clients[socket]
                continue
            user = clients[socket]

            print(f"Received message from {user}: {message} ")

            message_text = message['message'].decode('utf-8')

            if message['whom'].decode('utf-8') == 'All':
                for client_socket in clients:
                    if client_socket != socket:
                        send_message(user, 'All', message_text, client_socket)

            elif message['whom'].decode('utf-8') in username:
                to_user = message['whom'].decode('utf-8')
                send_message(user, to_user, message_text, username[to_user])

    for socket in exception_sockets:
        send_users_disconnect(socket)
        sockets_list.remove(socket)
        del username[clients[socket]]
        del clients[socket]
