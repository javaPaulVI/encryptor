import base64
import time
import os
import hmac
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


class Encryptor:
    SEPARATOR = "␟"  # Unicode U+241F, visible but rare

    def __init__(self, primary_key: str):
        if len(primary_key) < 6:
            raise ValueError("Primary key too short to modify as intended")
        self.primary_key = primary_key

    def generate_salt(self, minute: int) -> bytes:
        h = hmac.new(self.primary_key.encode(), str(minute).encode(), digestmod=hashes.SHA256().name)
        return h.digest()[:16]

    def derive_secondary_key(self, minute: int) -> bytes:
        salt = self.generate_salt(minute)
        modified_key = (
            self.primary_key[:4] + "6" +
            self.primary_key[5:-2] + "<" +
            self.primary_key[-1]
        )
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100_000,
            backend=default_backend()
        )
        derived = kdf.derive(modified_key.encode())
        return base64.urlsafe_b64encode(derived)

    def token_to_numbers(self, token: str) -> str:
        token_bytes = token.encode()
        number = int.from_bytes(token_bytes, byteorder='big')
        return str(number)

    def numbers_to_token(self, number_str: str) -> str:
        number = int(number_str)
        length = (number.bit_length() + 7) // 8
        token_bytes = number.to_bytes(length, byteorder='big')
        return token_bytes.decode('utf-8', errors='replace')

    def encrypt_message(self, message: str) -> str:
        current_minute = int(time.time() // 60)
        secondary_key = self.derive_secondary_key(current_minute)
        fernet = Fernet(secondary_key)
        payload = f"{current_minute}{self.SEPARATOR}{message}".encode()
        token = fernet.encrypt(payload).decode()
        b64 = base64.b64encode(token.encode()).decode()

        random_prefix = base64.b64encode(os.urandom(4)).decode().replace("=", "")
        xor_key = os.urandom(8)
        xored = bytes([b ^ xor_key[i % len(xor_key)] for i, b in enumerate(b64.encode())])
        hex_result = xored.hex()
        result = f"{random_prefix}{self.SEPARATOR}{base64.b64encode(xor_key).decode().replace('=','')}{self.SEPARATOR}{hex_result}"

        return self.token_to_numbers(result)

    def decrypt_message(self, encoded_token: str) -> tuple[str, int]:
        encoded_token = self.numbers_to_token(encoded_token)
        parts = encoded_token.split(self.SEPARATOR)
        if len(parts) != 3:
            raise ValueError("Invalid token format")

        _, xor_key_b64, hex_data = parts

        if len(xor_key_b64) % 4 != 0:
            xor_key_b64 += "=" * (4 - len(xor_key_b64) % 4)
        xor_key = base64.b64decode(xor_key_b64)

        xored_data = bytes.fromhex(hex_data)
        b64_bytes = bytes([b ^ xor_key[i % len(xor_key)] for i, b in enumerate(xored_data)])
        b64 = b64_bytes.decode(errors='replace')

        if len(b64) % 4 != 0:
            b64 += "=" * (4 - len(b64) % 4)

        token = base64.b64decode(b64).decode(errors='replace')

        current_minute = int(time.time() // 60)
        for minute_offset in range(-2, 3):
            try_minute = current_minute + minute_offset
            secondary_key = self.derive_secondary_key(try_minute)
            fernet = Fernet(secondary_key)
            try:
                payload = fernet.decrypt(token.encode()).decode()
                minute_str, message = payload.split(self.SEPARATOR, 1)
                return message, int(minute_str)
            except Exception:
                continue

        raise ValueError("Unable to decrypt with any valid minute key.")
