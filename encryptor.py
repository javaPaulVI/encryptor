import base64
import time
import os
import hmac
from datetime import datetime, timezone
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import sys


if sys.version_info >= (3, 11):
    sys.set_int_max_str_digits(0)


class Encryptor:
    __SEPARATOR = "␟"  

    def __init__(self, primary_key: str):
        self.__primary_key = primary_key

    def generate_salt(self, minute: int) -> bytes:
        h = hmac.new(self.__primary_key.encode(), str(minute).encode(), digestmod=hashes.SHA256().name)
        return h.digest()[:16]

    def derive_secondary_key(self, minute: int) -> bytes:
       salt = self.generate_salt(minute)
       minute_str = str(minute)
    
       kdf = PBKDF2HMAC(
           algorithm=hashes.SHA256(),
           length=32,
           salt=salt,
           iterations=100_000,
           backend=default_backend()
       )
       return base64.urlsafe_b64encode(kdf.derive(minute_str.encode()))

    def token_to_numbers(self, token: str) -> str:
        token_bytes = token.encode()
        number = int.from_bytes(token_bytes, byteorder='big')
        return str(number)

    def numbers_to_token(self, number_str: str) -> str:
        number = int(number_str)
        length = (number.bit_length() + 7) // 8
        token_bytes = number.to_bytes(length, byteorder='big')
        return token_bytes.decode('utf-8', errors='replace')

    def encrypt(self, message: str) -> str:
        current_minute = int(time.time() // 60)
        secondary_key = self.derive_secondary_key(current_minute)
        fernet = Fernet(secondary_key)
        payload = f"{current_minute}{self.__SEPARATOR}{message}".encode()
        token = fernet.encrypt(payload).decode()
        b64 = base64.b64encode(token.encode()).decode()

        random_prefix = base64.b64encode(os.urandom(4)).decode().replace("=", "")
        xor_key = os.urandom(8)
        xored = bytes([b ^ xor_key[i % len(xor_key)] for i, b in enumerate(b64.encode())])
        hex_result = xored.hex()

        # Include current_minute explicitly in the token
        result = f"{base64.b64encode(os.urandom(4)).decode().replace('=', '')}{self.__SEPARATOR}{base64.b64encode(xor_key).decode().replace('=', '')}{self.__SEPARATOR}{current_minute}{self.__SEPARATOR}{base64.b64encode(os.urandom(4)).decode().replace('=', '')}{self.__SEPARATOR}{hex_result}"
        return self.token_to_numbers(result)

    def decrypt(self, encoded_token: str) -> tuple[str, str]:
        encoded_token = self.numbers_to_token(encoded_token)
        parts = encoded_token.split(self.__SEPARATOR)
        if len(parts) != 5:
            raise ValueError("Invalid token format")

        # parts[0] and parts[3] are random and can be ignored
        _, xor_key_b64, minute_str, _, hex_data = parts

        # Pad Base64 if needed
        if len(xor_key_b64) % 4 != 0:
            xor_key_b64 += "=" * (4 - len(xor_key_b64) % 4)
        xor_key = base64.b64decode(xor_key_b64)

        try:
            encryption_minute = int(minute_str)
        except ValueError:
            raise ValueError("Invalid minute value in token")

        # Decode and XOR the hex-encoded payload
        xored_data = bytes.fromhex(hex_data)
        b64_bytes = bytes([b ^ xor_key[i % len(xor_key)] for i, b in enumerate(xored_data)])
        b64 = b64_bytes.decode(errors='replace')

        if len(b64) % 4 != 0:
            b64 += "=" * (4 - len(b64) % 4)

        token = base64.b64decode(b64).decode(errors='replace')

        # Use the embedded minute to derive the correct key
        secondary_key = self.derive_secondary_key(encryption_minute)
        fernet = Fernet(secondary_key)
        payload = fernet.decrypt(token.encode()).decode()
        _, message = payload.split(self.__SEPARATOR, 1)

        # Convert minute to human-readable UTC time string
        timestamp = encryption_minute * 60
        human_readable_time = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

        return message, human_readable_time


