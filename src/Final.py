import time
import huffman
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import re


# Compression
def compress_message(message):
    codec = huffman.codebook([(char, message.count(char)) for char in set(message)])
    compressed = ''.join(codec[char] for char in message)
    return compressed, codec


def decompress_message(compressed, codec):
    reverse_codec = {v: k for k, v in codec.items()}
    decompressed = ''
    buffer = ''
    for bit in compressed:
        buffer += bit
        if buffer in reverse_codec:
            decompressed += reverse_codec[buffer]
            buffer = ''
    return decompressed


# Encryption
def encrypt_data(data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data.encode()) + encryptor.finalize()
    return iv + encrypted


def decrypt_data(encrypted_data, key):
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted.decode()


# Embedding
SYNONYM_DICT = {
    'good': ('good', 'excellent'),
    'bad': ('bad', 'terrible'),
    'big': ('big', 'large'),
    'small': ('small', 'tiny'),
    'fast': ('fast', 'quick'),
    'slow': ('slow', 'sluggish'),
}


def embed_bits(cover_text, bits):
    words = cover_text.split()
    stego_words = []
    bit_index = 0

    for word in words:
        clean_word = re.sub(r'[^\w]', '', word.lower())

        if bit_index < len(bits) and clean_word in SYNONYM_DICT:
            word0, word1 = SYNONYM_DICT[clean_word]
            chosen = word1 if bits[bit_index] == '1' else word0

            if word[0].isupper():
                chosen = chosen.capitalize()
            if not word[-1].isalnum():
                chosen += word[-1]

            stego_words.append(chosen)
            bit_index += 1
        else:
            stego_words.append(word)

    return " ".join(stego_words)


def extract_bits(stego_text, original_cover, expected_bits_len):
    stego_words = stego_text.split()
    orig_words = original_cover.split()
    bits = ''

    for i in range(len(stego_words)):
        clean_orig = re.sub(r'[^\w]', '', orig_words[i].lower())

        if clean_orig in SYNONYM_DICT:
            word0, word1 = SYNONYM_DICT[clean_orig]
            clean_stego = re.sub(r'[^\w]', '', stego_words[i].lower())

            if clean_stego == word1.lower():
                bits += '1'
            elif clean_stego == word0.lower():
                bits += '0'

        if len(bits) >= expected_bits_len:
            break
    return bits[:expected_bits_len]


# Full Pipeline
def hide_message(secret_message, cover_text, key):
    print("=== HIDE MESSAGE DEBUG ===")

    # Compress
    compressed, codec = compress_message(secret_message)
    print(f"1. Compressed: {compressed}")
    print(f"   Length: {len(compressed)}")

    # Encrypt
    encrypted = encrypt_data(compressed, key)
    print(f"2. Encrypted bytes length: {len(encrypted)}")

    # Convert to bits
    bits = ''.join(format(byte, '08b') for byte in encrypted)
    print(f"3. Bits to embed: {bits[:50]}... (total: {len(bits)} bits)")

    # Embed
    stego_text = embed_bits(cover_text, bits)
    print(f"4. Stego text created (first 100 chars): {stego_text[:100]}")

    return stego_text, codec, len(bits)


def recover_message(stego_text, original_cover, codec, key, expected_bits_len):
    print("\n=== RECOVER MESSAGE DEBUG ===")

    # Extract bits
    bits = extract_bits(stego_text, original_cover, expected_bits_len)
    print(f"1. Extracted bits: {bits[:50]}... (total: {len(bits)} bits)")

    # Convert bits to bytes
    encrypted_bytes = bytearray()
    for i in range(0, len(bits), 8):
        byte_str = bits[i:i + 8]
        if len(byte_str) == 8:
            encrypted_bytes.append(int(byte_str, 2))

    print(f"2. Encrypted bytes length: {len(encrypted_bytes)}")

    # Decrypt
    decrypted_compressed = decrypt_data(bytes(encrypted_bytes), key)
    print(f"3. Decrypted compressed: {decrypted_compressed}")

    # Decompress
    original_message = decompress_message(decrypted_compressed, codec)
    print(f"4. Final message: {original_message}")

    return original_message


# Test
if __name__ == "__main__":
    secret_message = "India won th match"
    cover_text = "The good dog ran fast to the big house. The bad cat was slow and small. " * 200
    key = b'0123456789abcdef0123456789abcdef'

    # Hide
    stego_text, codec, bits_len = hide_message(secret_message, cover_text, key)

    # Recover
    recovered = recover_message(stego_text, cover_text, codec, key, bits_len)

    print(f"\n=== FINAL RESULT ===")
    print(f"Original: {secret_message}")
    print(f"Recovered: {recovered}")
    print(f"Match: {secret_message == recovered}")