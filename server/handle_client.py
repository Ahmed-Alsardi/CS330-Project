import logging
import socket

from shared.constants import ENCODE_FORMAT, HEADER_SIZE, DISCONNECT, REGULAR_MODE, SECRET_MODE
from shared.utils import calculate_message_length, decrypt_message, encrypt_message


class HandleClient:
    """
    A class that handle all the functionality of client who connected to the server
    """

    def __init__(self, client_socket: socket.socket, address, sending_mode: str = REGULAR_MODE):
        """
        Initialize of HandleClient class, then send a welcoming message for client
        :param client_socket:
        :param address:
        :param sending_mode: default mode is regular (or
        """
        self.socket_connection = client_socket
        self.address = address
        self.sending_mode = sending_mode
        # Send welcoming message
        self._send_message("Welcome to the Server")
        logging.info(f"SENDING]: welcome message to {self.address}")

    def run(self):
        """
        The main loop for handle client. running variable indicate user want to continue.
        exit the loop when running change to False.
        :return: None
        """
        running = True
        while running:
            # Start by listen for new message from user
            message = self._received_message()
            # check if the message is about changing the mode
            is_changed = self._handle_mode(message)
            if is_changed:
                # if the mood change, go to beginning of the loop
                continue
            # turn to running to False if the user want to quit
            if message == DISCONNECT:
                running = False
            logging.info(f"RECEIVED FROM {self.address}] Client send message: {message}")
            # return the same message upper case to the client
            self._send_message(message.upper())
        # close the connection
        self.socket_connection.close()

    def _received_message(self):
        """
        The protocol we use here is:
            1- The client will send first the length of message only , the first message have a fixed size buffer
            2- The server now will get the length from the first message, then the server
               will open buffer with the same length of the message
        :return: message: string
        """
        message_length = self.socket_connection.recv(HEADER_SIZE).decode(encoding=ENCODE_FORMAT)
        message_length = int(message_length)
        message = self.socket_connection.recv(message_length).decode(encoding=ENCODE_FORMAT)
        # check of the current mode is SECRET_MODE to decode the message
        if self.sending_mode == SECRET_MODE:
            print(f"received encrypted message from {self.address}: {message}")
            message = decrypt_message(message.encode(encoding=ENCODE_FORMAT))
        return message

    def _send_message(self, message: str):
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
            # Encrypt the message before calculate
            message = encrypt_message(message).decode(encoding=ENCODE_FORMAT)
            print(f"sending encrypted message from {self.address}: {message}")
        message_length = calculate_message_length(message)
        self.socket_connection.send(message_length)
        self.socket_connection.send(message.encode(encoding=ENCODE_FORMAT))

    def _handle_mode(self, message) -> bool:
        """
        Check if the message is about changing mode of the communication
        return True if the mode change
        :param message: str
        :return: bool
        """
        if message.upper() == REGULAR_MODE and self.sending_mode != REGULAR_MODE:
            self.sending_mode = REGULAR_MODE
            logging.info(f"CHANGE MODE TO {self.address}]: change to {REGULAR_MODE}")
            return True
        elif message.upper() == SECRET_MODE and self.sending_mode != SECRET_MODE:
            self.sending_mode = SECRET_MODE
            logging.info(f"CHANGE MODE TO {self.address}]: change to {SECRET_MODE}")
            return True
        return False


def handle_client(client_socket, client_address):
    """
    This method used by the server when creating a new thread for the client
    It create HandleClient class which handle all the functionality of single client
    :param client_socket
    :param client_address
    :return:
    """
    client = HandleClient(client_socket=client_socket, address=client_address)
    client.run()
    logging.info(f"QUIT]: Client with address {client.address}")
