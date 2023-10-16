#!/usr/bin/env python3

from typing import List
import binascii

SPACE = ord(' ')


def main():
    try:
        with open('ciphertext.txt', "r") as file:
            ciphertext_unformatted = [line.replace("b'", "").replace("'", "") for line in file]
            ciphertexts = [binascii.unhexlify(cipher.rstrip()) for cipher in ciphertext_unformatted]
    except Exception as e:
        raise SystemExit(-1)
    cleartexts = [bytearray(b'?' * len(line)) for line in ciphertexts]

    crack(ciphertexts, cleartexts)


def crack(ciphertexts: List[bytes], cleartexts: List[bytearray]) -> None:
    """ Try to decrypt ciphertexts and print cleartexts or key """
    max_length = max(len(line) for line in ciphertexts)
    key = bytearray(max_length)
    key_mask = [False] * max_length
    for column in range(max_length):  # go over characters from the beginning of lines
        pending_ciphers = [line for line in ciphertexts if len(line) > column]
        for cipher in pending_ciphers:
            if is_space(pending_ciphers, cipher[column], column):
                key[column] = cipher[column] ^ SPACE
                key_mask[column] = True
                i = 0
                for clear_row in range(len(cleartexts)):
                    if len(cleartexts[clear_row]) != 0 and column < len(cleartexts[clear_row]):
                        result = cipher[column] ^ pending_ciphers[i][column]
                        if result == 0:
                            cleartexts[clear_row][column] = SPACE
                        elif chr(result).isupper():  # XOR with space return letter with swapped case
                            cleartexts[clear_row][column] = ord(chr(result).lower())
                        elif chr(result).islower():  # XOR with space return letter with swapped case
                            cleartexts[clear_row][column] = ord(chr(result).upper())
                        i += 1
                break

    print('\n'.join(line.decode('ascii') for line in cleartexts))


def is_space(rows: List[bytes], current: int, column: int) -> bool:
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
