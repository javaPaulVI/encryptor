from encryptor import Encryptor
import os
import random
import secrets
import sys

def get_primary_key():
    KEY_FILE = ".primary_key"
    key = None
    if os.path.isfile(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            key = f.read().strip()
    else:
        print(f"Primary key file {KEY_FILE} not found. Creating {KEY_FILE} and generating a new key.")
        key = secrets.token_urlsafe(32)
        with open(KEY_FILE, "w") as f:
            f.write(key)

    if not key:
        key = secrets.token_urlsafe(32)
        print(f"Generated primary key: {key}")
        print(f"Saved primary key to {KEY_FILE}")
        print("For a custom primary key, change the content of the .primary_key file.")
        with open(KEY_FILE, "w") as f:
            f.write(key)
    return key



def main():
    primary_key = get_primary_key()
    try:
        encryptor = Encryptor(primary_key)
    except ValueError as e:
        print(f"Error: {e}")
        return

    while True:
        print("\nOptions:")
        print("1. Encrypt a message")
        print("2. Decrypt a token")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            file_content = False
            message = input("Enter message to encrypt: ").strip()
            if os.path.isfile(message):
                file_content = True
                with open(message, 'r') as file:
                    message = file.readlines()
                message = ''.join(message).strip()
            encrypted = encryptor.encrypt(message)
            print(f"\nEncrypted token:\n{encrypted+str(random.randint(0, 4)) if file_content else encrypted+str(random.randint(5, 9))}")
        elif choice == "2":
            file_content = False
            token = input("Enter token to decrypt: ").strip()
            try:
                if int(token[-1]) in range(0, 5):
                    file_content = True
                elif int(token[-1]) in range(5, 10):
                    file_content = False
                token = token[:-1]
                message, _ = encryptor.decrypt(token)
                print(f"\nDecrypted message: {message}" if not file_content else f"Decrypted message from File:\n\n{message}")
            except Exception as e:
                print(f"Decryption failed: {e}")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    exit_code=os.system('setup.bat' if os.name == 'nt' else 'setup.sh')
    if exit_code != 0:
        sys.exit(exit_code)
    os.system('cls' if os.name == 'nt' else 'clear')
    main()
