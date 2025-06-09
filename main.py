from encryptor import Encryptor
encryptor=Encryptor()
while True:
    cmd = input("(E)ncrypt or (D)ecrypt: ")
    if cmd.lower() == "e":
        print("Encrypted: "+ encryptor.encrypt_message(input("Enter Message: ")))
    elif cmd.lower() == "d":
        print("Decrypted: "+ encryptor.decrypt_message(input("Enter Message: ")))
    else:
        print("invalid input")

    print("\n")