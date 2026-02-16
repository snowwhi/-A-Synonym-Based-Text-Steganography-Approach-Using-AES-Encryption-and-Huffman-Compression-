
import huffman
secret_message = "Pakistan is going to win"
# Isolate compression test
def compress_message(message):
    # Encode the message using Huffman coding
    codec = huffman.codebook([(char, message.count(char)) for char in set(message)])
    compressed = ''.join(codec[char] for char in message)
    return compressed, codec  # Return compressed string and codec for decompression

compressed, codec = compress_message(secret_message)
print("Original:", secret_message)
print("Compressed (binary string):", compressed)
print("Codec:", codec)

def decompress_message(compressed, codec):
    # Decode using the codec
    reverse_codec = {v: k for k, v in codec.items()}
    decompressed = ''
    buffer = ''
    for bit in compressed:
        buffer += bit
        if buffer in reverse_codec:
            decompressed += reverse_codec[buffer]
            buffer = ''
    return decompressed
# Try to decompress immediately
decompressed = decompress_message(compressed, codec)
print("Decompressed:", decompressed)
