import logging
import socket
import threading

from handle_client import handle_client
from shared.constants import SERVER_ADDRESS, SERVER_PORT

# logging format
logging.basicConfig(level=logging.INFO, format='[%(asctime)s %(message)s', datefmt='%H:%M:%S')


class Server:
    """
    Server class have the responsibility of creating socket and
    listen for new client who want to connect. The server can manage multiple
    client by creating a new thread for each client
    """

    def __init__(self, server_address: str, server_port: int):
        """
        Initialize the socket
        :param server_address: IP the server
        :param server_port: port of the server
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((server_address, server_port))

    def run(self):
        """
        listen for new client, then create a new thread for each client.
        :return: None
        """
        self.server.listen()
        while True:
            client_socket, address = self.server.accept()
            logging.info(f"CLIENT CONNECTION]: Client connect with address {address}")
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.start()


if __name__ == '__main__':
    """
        SERVER_ADDRESS and SERVER_PORT this value imported from utils file to clean the code
    """
    server = Server(SERVER_ADDRESS, SERVER_PORT)
    logging.info(f"SERVER START]: Server listen at {SERVER_ADDRESS}")
    server.run()
