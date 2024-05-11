from pyDes import des, PAD_PKCS5
import binascii

def des_encrypt(message, key):
    # Convert the key from hex string to bytes
    print("Message before conversion:", message)
    print("Key before conversion:", key)
    key = binascii.unhexlify(key)
    # Create a DES object with the specified key
    sKey = des(key, PAD_PKCS5)
    # Encrypt the message
    ciphertext = sKey.encrypt(message)
    return binascii.hexlify(ciphertext).decode()

def main():
    # Input message and key
    message = input("Enter your message to encrypt: ").strip()
    key = input("Enter the encryption key: ").strip()

    # Check if the message and key are of the correct length
    if len(message) != 16 or len(key) != 16:
        print("Message and key should be 16 bytes (32 character).")
        return

    # Perform DES encryption for 16 rounds
    ciphertext = message
    for i in range(16):
        print(f"Round {i+1}:")
        ciphertext = des_encrypt(binascii.unhexlify(ciphertext), key)
        print("Ciphertext:", ciphertext)
        print()

if __name__ == "__main__":
    main()
