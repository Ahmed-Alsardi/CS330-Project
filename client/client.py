import logging
import socket

from shared.constants import (SERVER_PORT, SERVER_ADDRESS,
                              HEADER_SIZE, ENCODE_FORMAT,
                              DISCONNECT, REGULAR_MODE, SECRET_MODE)
from shared.utils import calculate_message_length, encrypt_message, decrypt_message

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(message)s', datefmt='%H:%M:%S')


class Client:

    def __init__(self, server_address, server_port, sending_mode: str = REGULAR_MODE):
        self.client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connection.connect((server_address, server_port))
        self.sending_mode = sending_mode
        message_length = self.client_connection.recv(HEADER_SIZE)
        message_length = int(message_length)
        welcome_message = self.client_connection.recv(message_length).decode(encoding=ENCODE_FORMAT)
        logging.info(f"RECEIVE MESSAGE]: {welcome_message}")

    def run(self):
        running = True
        while running:
            # TODO: Change the mode if the user chose from the following
            print(f"TYPE {DISCONNECT} for closing connection\n"
                  f"\t{REGULAR_MODE} for changing mode to regular\n"
                  f"\t{SECRET_MODE} for changing mode to secret")
            input_message = input("Enter your message here: ")
            is_changed = self._handle_mode(input_message)
            if is_changed:
                continue
            input_message = self._send_message(input_message)
            if input_message == DISCONNECT:
                running = False
            message = self._received_message()
            logging.info(f"RECEIVED]: Received message from server: {message}")
        self.client_connection.close()

    def _send_message(self, message) -> str:
        # TODO: Check for mode before sending
        if self.sending_mode == SECRET_MODE:
            message = encrypt_message(message).decode(encoding=ENCODE_FORMAT)
            print(f"sending encrypted message: {message}")
        message_length = calculate_message_length(message)
        self.client_connection.send(message_length)
        self.client_connection.send(message.encode(encoding=ENCODE_FORMAT))
        return message

    def _received_message(self) -> str:
        message_length = self.client_connection.recv(HEADER_SIZE)
        message_length = int(message_length)
        message = self.client_connection.recv(message_length).decode(encoding=ENCODE_FORMAT)
        if self.sending_mode == SECRET_MODE:
            print(f"received encrypted message: {message}")
            message = decrypt_message(message.encode(encoding=ENCODE_FORMAT))
        return message

    def _handle_mode(self, message) -> bool:
        if message.upper() == REGULAR_MODE and self.sending_mode != REGULAR_MODE:
            # Change the mode in the server to
            self._send_message(REGULAR_MODE)
            self.sending_mode = REGULAR_MODE
            logging.info(f"CHANGE MODE]: change to {REGULAR_MODE}")
            return True
        elif message.upper() == SECRET_MODE and self.sending_mode != SECRET_MODE:
            self._send_message(SECRET_MODE)
            self.sending_mode = SECRET_MODE
            logging.info(f"CHANGE MODE]: change to {SECRET_MODE}")
            return True
        return False


if __name__ == '__main__':
    client_connection = Client(server_address=SERVER_ADDRESS, server_port=SERVER_PORT)
    client_connection.run()
    logging.info(f"CLOSE]: Connection is closed")
