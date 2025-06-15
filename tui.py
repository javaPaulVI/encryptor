from encryptor import Encryptor
import os
import random


def main():
    primary_key = None
    with open(".primary_key", "r") as f:
        primary_key = f.read().strip()
    if not primary_key:
        print("Error: PRIMARY_KEY environment variable not set.")
        return
    print(f"Using primary key: {primary_key}")
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
                with open(message, 'r') as file:
                    message = file.readlines()
                message = ''.join(message).strip()
            encrypted = encryptor.encrypt_message(message)
            print(f"\nEncrypted token:\n{encrypted+str(random.randint(0, 4)) if file_content else encrypted+str(random.randint(5, 9))}")
        elif choice == "2":
            file_content = False
            token = input("Enter token to decrypt: ").strip()
            try:
                message,_ = encryptor.decrypt_message(token)
                if int(token[-1]) in range(0, 5):
                    file_content = True
                elif int(token[-1]) in range(5, 10):
                    file_content = False
                token = token[:-1]
                print(f"\nDecrypted message: {message}" if not file_content else f"Decrypted message from File:\n\n{message}")
            except Exception as e:
                print(f"Decryption failed: {e}")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
