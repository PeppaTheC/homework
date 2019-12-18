"""This module contains GUI realization of chat."""

from client import Client

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog


class ChatEnter(QDialog):
    """Enter window.

    Opens the start dialog box for entering a user name.
    And emits a close signal to the main window with contents of the username.
    """
    set_name = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi('chat_enter.ui', self)
        self.pushButtonEnter.clicked.connect(self.close)

    def closeEvent(self, _):
        """Close callback. Send to main window the entered name"""
        self.set_name.emit(self.lineEditUsername.text())

    def keyPressEvent(self, event) -> None:
        """Enter pressed callback"""
        enter_key = 16777220
        if event.key() == enter_key:
            self.close()


class Chat(QMainWindow):
    """GUI chat implementation

    Attributes:
        current_user: index for users lists of current chosen user in
                      list widget
        users_list: list of online users
        users_message_history: message history for each user to each user
        client: instance of client.Client, which provides
                communication protocol with server
        username: user name

    """
    __slots__ = {
        'current_user',
        'users_list',
        'users_message_history',
        'client',
        'username',
    }

    send_message = pyqtSignal(str, str)  # send signal to Client

    def __init__(self):
        super().__init__()
        uic.loadUi('frontend.ui', self)
        self.username = None
        self.open_chat_enter_window()

        if self.username:
            self.users_list = ['All']
            self.current_user = 0
            self.users_message_history = ['']
            self.client = Client(self.username)

            self.listWidgetUsersOnline.currentRowChanged.connect(self.current_user_changed)
            self.pushButtonSendMessage.clicked.connect(self.clicked_send_message)

            self.client.get_message.connect(self.handle_message)
            self.client.get_server_message.connect(self.handle_server_message)
            self.send_message.connect(self.client.send_message)
            self.client.start()

    @pyqtSlot(str)
    def set_username(self, text: str):
        """Slot for username change"""
        self.username = text

    def open_chat_enter_window(self):
        """Open enter window """
        chat_enter = ChatEnter()
        chat_enter.set_name.connect(self.set_username)
        chat_enter.exec()

    def current_user_changed(self, row: int):
        """Slot for user changed in list widget"""
        self.current_user = row
        self.plainTextEditChat.setPlainText(self.users_message_history[self.current_user].rstrip())

    def clicked_send_message(self):
        """Callback send message button clicked.

        Adds the entered text to the user's correspondence history,
        displays the text on the screen and sends it to the selected user.
        """
        text = self.lineEditMessageText.text()
        if text:
            self.send_message.emit(self.users_list[self.current_user], text)
            message = f"You: {text}"
            self.plainTextEditChat.appendPlainText(message)
            self.users_message_history[self.current_user] += message + '\n'
            self.lineEditMessageText.clear()

    @pyqtSlot(dict)
    def handle_message(self, data: dict):
        """Slot for receiving users messages

        Adds the received text to the user's correspondence history,
        displays the text on the screen.

        Args:
            data: dict contains from who message is and the message it self
        """
        sender = data['from_who'].decode('utf-8')
        message = f"{sender}: {data['message'].decode('utf-8')}"
        user = self.users_list.index(sender) if data['whom'] != b'All' else 0
        if user == self.current_user:
            self.plainTextEditChat.appendPlainText(message)
        self.users_message_history[user] += message + '\n'

    @pyqtSlot(dict)
    def handle_server_message(self, data: dict):
        """Slot for receiving users messages

        Remove disconnected users for chat
        and adds new users to chat.

        Args:
            data: dict contains server command ('whom')
                  1 - add new user
                  2 - delete user
                  user ('message') - username to be removed or added

        """
        command = data['whom'].decode('utf-8')
        user = data['message'].decode('utf-8')
        if command == '1':
            self.listWidgetUsersOnline.addItem(user)
            self.users_list.append(user)
            self.users_message_history.append('')
        if command == '2':
            disconnected_user = self.users_list.index(user)
            self.listWidgetUsersOnline.takeItem(disconnected_user)
            if disconnected_user == self.current_user:
                self.listWidgetUsersOnline.setCurrentItem(0)
                self.plainTextEditChat.setPlainText(self.users_message_history[0])
            self.users_list.remove(user)

    def keyPressEvent(self, event) -> None:
        """Callback for pressed enter"""
        enter_key = 16777220
        if event.key() == enter_key:
            self.clicked_send_message()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    chat = Chat()
    chat.show()
    sys.exit(app.exec_())
