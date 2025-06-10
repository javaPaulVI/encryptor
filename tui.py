from encryptor import Encryptor
import os


def main():
    primary_key = os.environ.get('PRIMARY_KEY')
    if not primary_key:
        print("Error: PRIMARY_KEY environment variable not set.")
        return

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
            message = input("Enter message to encrypt: ").strip()
            encrypted = encryptor.encrypt_message(message)
            print(f"\nEncrypted token:\n{encrypted}")
        elif choice == "2":
            token = input("Enter token to decrypt: ").strip()
            try:
                message,_ = encryptor.decrypt_message(token)
                print(f"\nDecrypted message: {message}")
            except Exception as e:
                print(f"Decryption failed: {e}")
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
