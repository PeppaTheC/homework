"""This module contains realization of TCP Client

Client can receive and send messages to server by TCP/IP protocol.
"""

import socket as sock
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot

HEADER_LENGTH = 10
IP = '192.168.56.1'
PORT = 9000


class Client(QThread):
    __slots__ = {'client_socket',
                 'username',
                 'username_header'}

    get_message = pyqtSignal(dict)
    get_server_message = pyqtSignal(dict)

    def __init__(self, name: str):
        super().__init__()
        self.client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))
        self.client_socket.setblocking(True)

        self.username = name.encode('utf-8')
        self.username_header = self.get_header(self.username)

        self.client_socket.send(self.username_header + self.username)
        self.username = self.receive_user_name(self.client_socket)
        self.username_header = self.get_header(self.username)

    @staticmethod
    def get_header(text: bytes):
        return f"{len(text):<{HEADER_LENGTH}}".encode('utf-8')

    def run(self) -> None:
        while True:
            data = self.receive_user_message()
            if data is False:
                break
            if data['from_who'] == b'host':
                self.get_server_message.emit(data)
                continue
            self.get_message.emit(data)

    @pyqtSlot(str, str)
    def send_message(self, whom: str, message: str) -> None:
        whom = whom.encode('utf-8')
        message = message.encode('utf-8')
        whom_header = self.get_header(whom)
        message_header = self.get_header(message)
        self.client_socket.send(self.username_header + self.username + whom_header + whom + message_header + message)

    def receive_user_message(self):
        from_who = self.receive_data(self.client_socket)
        whom = self.receive_data(self.client_socket)
        message = self.receive_data(self.client_socket)
        if whom and message:
            return {'from_who': from_who, 'whom': whom, 'message': message}
        return False

    def receive_user_name(self, client_socket: sock.socket):
        return self.receive_data(client_socket)

    @staticmethod
    def receive_data(client_socket: sock.socket):
        try:
            message_header = client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                return False
            message_length = int(message_header.decode('utf-8').strip())
            return client_socket.recv(message_length)
        except (ValueError, sock.error,):
            return False


if __name__ == '__main__':
    client = Client('ivan')
    client.send_message('a', 'privet')
