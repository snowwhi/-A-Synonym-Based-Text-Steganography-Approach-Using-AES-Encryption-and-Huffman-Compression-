from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os


# Step 2: Encryption Module using AES-CTR
def encrypt_data(data, key):
    # Key should be 32 bytes for AES-256
    iv = os.urandom(16)  # Initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data.encode()) + encryptor.finalize()
    return iv + encrypted  # Prepend IV for decryption


def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted.decode()


# Test encryption/decryption
if __name__ == "__main__":
    compressed = "0001101001101100010000111110001011111100011011101"
    key = b'0123456789abcdef0123456789abcdef'

    # Encrypt
    encrypted = encrypt_data(compressed, key)
    print("Compressed (original):", compressed)
    print("Encrypted (bytes):", encrypted)
    print("Encrypted length:", len(encrypted))

    # Decrypt
    decrypted = decrypt_data(encrypted, key)
    print("Decrypted:", decrypted)

    # Check if they match
    print("Match:", compressed == decrypted)