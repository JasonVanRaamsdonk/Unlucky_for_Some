""""
author: @JasonVanRaamsdonk
"""
import binascii
import collections
import hashlib
import string
import codecs

decode_hex = codecs.getdecoder("hex_codec")

target_ciphertext = "a0e0d07be0de55e3e89ea0368ff9967b00bb76a043a70ff45faec908f4c3eae0bc84653cbd99ed50c2c53df892a14c7b8a51e66920766d233ffcebb327c15b7af51ee58d4b4bf831f32f3cda1405d9b5bf6c1a07a5ce4692f533643d03ab9ee77d28ac6f510ff8a0fa80de52788107f0fe3b83518d7b64038329e2ed6b6f8dd8cad23f49edb9426c5c4b864f25e2971a56054861a6d7d4fbac5220ce98b5ac65458ddaf3"


def xor(string_1, string_2):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(string_1, string_2)])


ciphertexts = []
key = [None]*400
known_key_positions = set()

with open('ciphertext.txt', 'r') as file:
    for line in file:
        hex_string = line.strip().lstrip('b').strip("'")
        ciphertexts.append(hex_string)

# ciphertexts = [binascii.hexlify(bytes(line, 'utf-8')) for line in hex_ciphertext]
# print(ciphertexts)
# print(hex_ciphertext)
# cleartext = [bytearray(b'?' * len(line)) for ciphertext in ciphertexts]
# print(cleartext)
# print(ciphertexts)

for i, ciphertext in enumerate(ciphertexts):
    counter = collections.Counter()

    for j, ciphertext_2 in enumerate(ciphertexts):
        if i != j:  # to avoid xoring a ciphertext with itself
            xor_ciphertext = xor(ciphertext, ciphertext_2)  # xoring 2 different ciphertexts
            for character_index, char in enumerate(xor_ciphertext):
                if char in string.printable and char.isalpha():
                    counter[character_index] += 1

    space_indexes = []

    for space_index, value in counter.items():
        if value >= 7:
            space_indexes.append(space_index)

    xor_space_w_ciphertext = xor(ciphertext, ' '*400)

    for index in space_indexes:
        key[index] = xor_space_w_ciphertext[index]
        known_key_positions.add(index)


hex_key = ''.join([value if value is not None else '00' for value in key])
output = xor(target_ciphertext, hex_key)
print(''.join([char if index in known_key_positions else '*' for index, char in enumerate(output)]))

final_key = xor(target_ciphertext, )
for cipher in ciphertexts:
    print(xor(cipher, key))
