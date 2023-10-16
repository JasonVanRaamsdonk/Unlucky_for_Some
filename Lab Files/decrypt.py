""""
author: @JasonVanRaamsdonk
"""
import binascii
import hashlib

hex_ciphertext = []

with open('ciphertext.txt', 'r') as file:
    for line in file:
        hex_string = line.strip().lstrip('b').strip("'")
        hex_ciphertext.append(hex_string)

ciphertext = [binascii.hexlify(bytes(line, 'utf-8')) for line in hex_ciphertext]
# print(ciphertext)
cleartext = [bytearray(b'?' * len(line)) for line in ciphertext]
# print(cleartext)

