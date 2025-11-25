def caesar(plaintext, cipherkey):

    # Local variables
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    ciphertext = ""
    

    # Shift each letter in the plaintext by the value of "cipherkey"
    for i in range (len(plaintext)):
        idx = alphabet.index(plaintext[i])

        # Wrap around at top on encrypt
        idx = (idx + cipherkey) % len(alphabet)

        # Prevent underflow on decrypt
        if idx < 0:
            idx += len(alphabet)

        # Apply shift to the character
        ciphertext = ciphertext + alphabet[idx]

    return ciphertext
