import logging
import socket

from shared.constants import (SERVER_PORT, SERVER_ADDRESS,
                              HEADER_SIZE, ENCODE_FORMAT,
                              DISCONNECT, REGULAR_MODE, SECRET_MODE)
from shared.utils import calculate_message_length, encrypt_message, decrypt_message

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(message)s', datefmt='%H:%M:%S')


class Client:
    """
    Client class for handling all functionality of sending and receiving
    between client and server.
    """

    def __init__(self, server_address, server_port, sending_mode: str = REGULAR_MODE):
        """
        Connect with the server with given address and port, then listen for the welcoming message
        :param server_address
        :param server_port
        :param sending_mode: default to regular mode
        """
        self.client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connection.connect((server_address, server_port))
        self.sending_mode = sending_mode
        message_length = self.client_connection.recv(HEADER_SIZE)
        message_length = int(message_length)
        welcome_message = self.client_connection.recv(message_length).decode(encoding=ENCODE_FORMAT)
        logging.info(f"RECEIVE MESSAGE]: {welcome_message}")

    def run(self):
        """
        The main loop for client. running variable indicate user want to continue.
        exit the loop when running change to False.
        :return: None
        """
        running = True
        while running:
            # List the available actions
            print("Type:\n",
                  f"\t{REGULAR_MODE}) for changing mode to regular\n,"
                  f"\t{SECRET_MODE}) for changing mode to secret\n",
                  f"\t{DISCONNECT}) for closing connection\n"
                  )
            input_message = input("Enter your message here: ")
            # Check if the user change the mode
            is_changed = self._handle_mode(input_message)
            if is_changed:
                continue
            # send the message to server
            input_message = self._send_message(input_message)
            # quit if the user choose to disconnect
            if input_message == DISCONNECT:
                running = False
            # receive the message from server
            message = self._received_message()
            logging.info(f"RECEIVED]: Received message from server: {message}")
        # close the connection
        self.client_connection.close()

    def _send_message(self, message) -> str:
        """
        Steps:
            1- Check if the mode is SECRET
            2- calculate the length of message.
            3- Send the message to client about the length.
            4- Send the message to client.
        :param message: string
        :return: None
        """
        if self.sending_mode == SECRET_MODE:
            message = encrypt_message(message).decode(encoding=ENCODE_FORMAT)
            print(f"sending encrypted message: {message}")
        message_length = calculate_message_length(message)
        self.client_connection.send(message_length)
        self.client_connection.send(message.encode(encoding=ENCODE_FORMAT))
        return message

    def _received_message(self) -> str:
        """
        The protocol we use here is:
            1- The server will send first the length of message only, the first message have a fixed size buffer
            2- The client now will get the length from the first message, then the client
               will open buffer with the same length of the message
        :return: message: string
        """
        message_length = self.client_connection.recv(HEADER_SIZE)
        message_length = int(message_length)
        message = self.client_connection.recv(message_length).decode(encoding=ENCODE_FORMAT)
        if self.sending_mode == SECRET_MODE:
            print(f"received encrypted message: {message}")
            message = decrypt_message(message.encode(encoding=ENCODE_FORMAT))
        return message

    def _handle_mode(self, message) -> bool:
        """
        Check if the user change the mode, if the mode change; send the update to server.
        :param message:
        :return: bool
        """
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
