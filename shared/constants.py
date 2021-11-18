SERVER_ADDRESS = "localhost"
SERVER_PORT = 5000
HEADER_SIZE = 64
ENCODE_FORMAT = "utf-8"
DISCONNECT = "DISCONNECT!"


def calculate_message_length(message: str) -> bytes:
    message_length = f"{len(message):<{HEADER_SIZE}}"
    return message_length.encode(encoding=ENCODE_FORMAT)
