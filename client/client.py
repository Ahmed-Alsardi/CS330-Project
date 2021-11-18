import logging
import socket

from shared.constants import (SERVER_PORT, SERVER_ADDRESS,
                              HEADER_SIZE, ENCODE_FORMAT,
                              calculate_message_length, DISCONNECT)

logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(message)s', datefmt='%H:%M:%S')


class Client:

    def __init__(self, server_address, server_port):
        self.client_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_connection.connect((server_address, server_port))
        message_length = self.client_connection.recv(HEADER_SIZE)
        message_length = int(message_length)
        welcome_message = self.client_connection.recv(message_length).decode(encoding=ENCODE_FORMAT)
        logging.info(f"RECEIVE MESSAGE]: {welcome_message}")

    def run(self):
        running = True
        while running:
            input_message = input("Enter your message here: ")
            message_length = calculate_message_length(input_message)
            self.client_connection.send(message_length)
            self.client_connection.send(input_message.encode(encoding=ENCODE_FORMAT))
            if input_message == DISCONNECT:
                running = False
        self.client_connection.close()


if __name__ == '__main__':
    client_connection = Client(server_address=SERVER_ADDRESS, server_port=SERVER_PORT)
    client_connection.run()
    logging.info(f"CLOSE]: Connection is closed")
