from Crypto.Cipher import ChaCha20
from Crypto.Random import get_random_bytes
from Crypto.Util.number import *

def encrypt(key, nonce, pt):
    chacha = ChaCha20.new(key=key, nonce=nonce)
    return chacha.encrypt(pt)

def main():
    lines = open("messages.txt", "rb").readlines()
    key = get_random_bytes(32)
    nonce = get_random_bytes(8)
    lines = [x.ljust(162) for x in lines]
    lines = [(encrypt(key, nonce, x)).hex().encode() for x in lines]
    #open("ciphertext.txt", "wb").write(b'\n'.join(line) for line in lines)
    with open('ciphertext.txt', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(str(line) for line in lines))
if __name__ == "__main__":
    main()
