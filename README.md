# UDP Backdoor

This is a proof of concept backdoor written in Python.

It listens on a UDP socket. This is because discovering UDP services using a
network scanner is more difficult than discovering TCP services since it is
connectionless. The backdoor currently doesn't send any data in response but
allows you to send a command that will be executed using `os.system`. The
output of the command is not echoed to you, but you could always use this to
spawn another reverse shell or whatever. The command is encrypted using AES,
I should probably add more code to make sure the SECRET_KEY is good enough, but
I'm just typing this so I can commit and go to sleep.

## Important
Change the SECRET_KEY in both the client and backdoor to something good.

## Considerations and Caveats
This is just a stupid backdoor that takes the `MESSAGE` from `dgram_client_unprivledged.py`, encrypts it, sends it to the server, decrypts it,
and then executes it using `os.system`. Both the client and server have constants
for the port numbers and IP addresses that will need to be changed. You need to
change the payload for the command you execute.

## Why is this unprivileged and what is the difference
This _can_ be used by both unprivileged and privileged users. The reason I say
unprivileged is because this is a slightly lamer version of what I wanted to do
but I'm sick at the moment. This uses a UDP socket, which an unprivileged user can create provided the port number is unprivileged.

What I _wanted_ to do was use a raw socket and no matter what send an ICMP Type
3 port unavailable response so even if a scanner scans it the port would appear
closed. I don't have the will to read at the moment, but this should be easy
using a raw socket and SCAPY to simulate the ICMP response.

There's obviously a lot that can be added to make this better, but it might not
even be worth it since you can prolly just emulate this by chaining nc and
openssl or whatever or using socat and python probably isn't the best choice for a backdoor but now this exists and maybe ill work on it when I'm not feeling well again.

Yes its totally fine to send the IV in the message. You need it and its better
than hardcoding it.

Ok cool I think that sums it up, feel free to open an issue if you actually see
this and care strongly about something.

## Installation
1. `git clone https://github.com/mynameiswillporter/udp_backdoor.git`
2. `cd udp_backdoor`
3. `python3 -m venv venv`
4. Activate your venv depending on os, maybe `. venv/bin/activate` on linux or `venv\Scripts\activate` on windows.
5. `pip install -r requirements.txt`

## Running
Install the code, activate your venv etc.
