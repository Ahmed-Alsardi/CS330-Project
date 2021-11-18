import logging
import socket

from shared.constants import ENCODE_FORMAT, HEADER_SIZE, DISCONNECT, REGULAR_MODE, SECRET_MODE
from shared.utils import calculate_message_length, decrypt_message, encrypt_message


class HandleClient:
    def __init__(self, client_socket: socket.socket, address, sending_mode: str = REGULAR_MODE):
        self.socket_connection = client_socket
        self.address = address
        self.sending_mode = sending_mode
        self._send_message("Welcome to the Server")
        logging.info(f"SENDING]: welcome message to {self.address}")

    def run(self):
        running = True
        while running:
            message = self._received_message()
            is_changed = self._handle_mode(message)
            if is_changed:
                continue
            if message == DISCONNECT:
                running = False
            # return the same message all upper case for now
            logging.info(f"RECEIVED] Client send message: {message}")
            self._send_message(message.upper())
        self.socket_connection.close()

    def _received_message(self):
        message_length = self.socket_connection.recv(HEADER_SIZE).decode(encoding=ENCODE_FORMAT)
        message_length = int(message_length)
        message = self.socket_connection.recv(message_length).decode(encoding=ENCODE_FORMAT)
        if self.sending_mode == SECRET_MODE:
            print(f"received encrypted message: {message}")
            message = decrypt_message(message.encode(encoding=ENCODE_FORMAT))
        return message

    def _send_message(self, message: str):
        # TODO: check for mode before sending
        if self.sending_mode == SECRET_MODE:
            message = encrypt_message(message).decode(encoding=ENCODE_FORMAT)
            print(f"sending encrypted message: {message}")
        message_length = calculate_message_length(message)
        self.socket_connection.send(message_length)
        self.socket_connection.send(message.encode(encoding=ENCODE_FORMAT))

    def _handle_mode(self, message) -> bool:
        if message.upper() == REGULAR_MODE and self.sending_mode != REGULAR_MODE:
            self.sending_mode = REGULAR_MODE
            logging.info(f"CHANGE MODE]: change to {REGULAR_MODE}")
            return True
        elif message.upper() == SECRET_MODE and self.sending_mode != SECRET_MODE:
            self.sending_mode = SECRET_MODE
            logging.info(f"CHANGE MODE]: change to {SECRET_MODE}")
            return True
        return False


def handle_client(client_socket, client_address):
    client = HandleClient(client_socket=client_socket, address=client_address)
    client.run()
    logging.info(f"QUIT]: Client with address {client.address}")
