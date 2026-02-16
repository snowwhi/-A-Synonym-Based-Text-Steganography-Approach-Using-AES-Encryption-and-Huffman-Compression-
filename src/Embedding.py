import re

# Synonym dictionary
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

            # Preserve Capitalization
            if word[0].isupper():
                chosen = chosen.capitalize()
            # Preserve Punctuation
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


# Test embedding/extraction
if __name__ == "__main__":
    # Simulating encrypted bytes converted to bits
    test_bits = "0001101001101100010000111110001011111100011011101"

    cover_text = "The good dog ran fast to the big house. The bad cat was slow and small. " * 50

    print("Original bits:", test_bits)
    print("Bits length:", len(test_bits))
    print("Cover text length:", len(cover_text))

    # Embed
    stego_text = embed_bits(cover_text, test_bits)
    print("\nFirst 200 chars of stego text:", stego_text[:200])

    # Extract
    extracted_bits = extract_bits(stego_text, cover_text, len(test_bits))
    print("\nExtracted bits:", extracted_bits)
    print("Extracted bits length:", len(extracted_bits))

    # Check match
    print("\nMatch:", test_bits == extracted_bits)

