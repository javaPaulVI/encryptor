import base64
import time
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


class Encryptor:
    def __init__(self):
        self.PRIMARY_KEY = "SM<iek-nQf5H+-yEu"

    def __derive_secondary_key(self, primary_key: str, minute: int) -> bytes:
        salt = str(minute * 7919).encode()[:8]
        if len(primary_key) < 6:
            raise ValueError("Primary key too short to modify as intended")
        modified_key = (
            primary_key[:4] + "6" +  
            primary_key[5:-2] + "<" +
            primary_key[-1]
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

    def encrypt_message(self, message: str) -> str:
        current_minute = int(time.time() // 60)
        secondary_key = self.__derive_secondary_key(self.PRIMARY_KEY, current_minute)
        fernet = Fernet(secondary_key)
        token = fernet.encrypt(message.encode()).decode()

        combined = f"{current_minute}\x1F{token}".encode()
        b64 = base64.b64encode(combined).decode()

        return b64.rstrip("=")


    def decrypt_message(self, encoded_token: str) -> str:
        try:
            padding = 4 - (len(encoded_token) % 4)
            if padding != 4:
                encoded_token += "=" * padding

            decoded = base64.b64decode(encoded_token).decode()
            minute_str, enc = decoded.split("\x1F", 1)
            minute = int(minute_str)

            secondary_key = self.__derive_secondary_key(self.PRIMARY_KEY, minute)
            fernet = Fernet(secondary_key)
            decrypted = fernet.decrypt(enc.encode()).decode()
            return decrypted
        except Exception as e:
            return f"Decryption failed\n {e}"
