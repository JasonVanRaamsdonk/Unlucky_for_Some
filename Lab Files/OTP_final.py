"""
@JasonVanRaamsdonk

"""
import time
from typing import List
import binascii
from xor_example import XORStrings
import codecs

SPACE = ord(' ')


def main():
    ciphertexts = format_file_input('ciphertext.txt')
    cleartexts = [bytearray(b'?' * len(line)) for line in ciphertexts]

    crack_manytimepad(ciphertexts, cleartexts)


def format_file_input(filename):
    try:
        with open(filename, "r") as file:
            ciphertext_unformatted = [line.replace("b'", "").replace("'", "") for line in file]
            print(f'formatting ciphertext file...')
            time.sleep(0.1)
            ciphertexts = [binascii.unhexlify(cipher.rstrip()) for cipher in ciphertext_unformatted]
            print(f'translating binary data to hex representation...')
            time.sleep(0.1)
            return ciphertexts
    except Exception:
        raise SystemExit(-1)


def crack_manytimepad(ciphertexts: List[bytes], cleartexts: List[bytearray]):
    """ Try to decrypt ciphertexts and print cleartexts or key """
    max_length = max(len(line) for line in ciphertexts)
    key = bytearray(max_length)
    key_mask = [False] * max_length
    time.sleep(0.1)
    print(f'attempting to crack Many-Time-Pad ciphers...\n')
    for column in range(max_length):  # go over characters from the beginning of lines
        remaining_ciphers = [line for line in ciphertexts if len(line) > column]
        for cipher in remaining_ciphers:
            if is_valid_value(remaining_ciphers, cipher[column], column):
                key[column] = cipher[column] ^ SPACE
                key_mask[column] = True
                index = 0
                for clear_text in range(len(cleartexts)):
                    if len(cleartexts[clear_text]) != 0 and column < len(cleartexts[clear_text]):
                        xor_value = cipher[column] ^ remaining_ciphers[index][column]
                        if xor_value == 0:
                            cleartexts[clear_text][column] = SPACE
                        elif chr(xor_value).isupper():  # XOR with space return letter with swapped case
                            cleartexts[clear_text][column] = ord(chr(xor_value).lower())
                        elif chr(xor_value).islower():  # XOR with space return letter with swapped case
                            cleartexts[clear_text][column] = ord(chr(xor_value).upper())
                        index += 1
                    else:
                        break

    for index, line in enumerate(cleartexts):
        time.sleep(0.1)
        # print(f'ciphertext {index + 1}: ')
        print('->  ', (line.decode('utf-8')))


def is_valid_value(rows: List[bytes], current: int, column: int):
    """
    Return whether the current byte is encrypted space
    If the current byte is space, XORing with other bytes should return alpha char or zero (when space)
    """
    for row in rows:
        result = row[column] ^ current
        if not (chr(result).isalpha() or result == 0):
            return False
    return True


if __name__ == '__main__':
    main()
