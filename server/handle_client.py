import logging
import socket

from shared.constants import calculate_message_length, ENCODE_FORMAT, HEADER_SIZE, DISCONNECT


class HandleClient:
    def __init__(self, client_socket: socket.socket, address):
        self.socket_connection = client_socket
        self.address = address
        welcome_message = "WELCOME TO THE SERVER"
        message_length = calculate_message_length(welcome_message)
        self.socket_connection.send(message_length)
        self.socket_connection.send(welcome_message.encode(encoding=ENCODE_FORMAT))
        logging.info(f"SENDING]: welcome message to {self.address}")

    def run(self):
        running = True
        while running:
            message = self._received_message()
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
        return message

    def _send_message(self, message: str):
        message_length = calculate_message_length(message)
        self.socket_connection.send(message_length)
        self.socket_connection.send(message.encode(encoding=ENCODE_FORMAT))


def handle_client(client_socket, client_address):
    client = HandleClient(client_socket=client_socket, address=client_address)
    client.run()
    logging.info(f"QUIT]: Client with address {client.address}")
