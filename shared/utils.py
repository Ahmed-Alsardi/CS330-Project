from cryptography.fernet import Fernet

from shared.constants import HEADER_SIZE, ENCODE_FORMAT

SECRET_KEY = "t8JbqtzCBh5df56RPD0XfvStnoc5pAZSKjt6ONPDI78="


def calculate_message_length(message: str) -> bytes:
    message_length = f"{len(message):<{HEADER_SIZE}}"
    return message_length.encode(encoding=ENCODE_FORMAT)


def encrypt_message(message: str) -> bytes:
    fernet = Fernet(SECRET_KEY)
    encrypted_message = fernet.encrypt(message.encode(encoding=ENCODE_FORMAT))
    return encrypted_message


def decrypt_message(encrypted_message: bytes) -> str:
    fernet = Fernet(SECRET_KEY)
    message = fernet.decrypt(encrypted_message).decode(encoding=ENCODE_FORMAT)
    return message
