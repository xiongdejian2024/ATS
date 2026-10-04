
import socket
import time


class UdpSocketClient:
    def __init__(self, name, address=("172.16.5.1", 30502), sock=None):
        self.name = name
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.sock = sock
        self.sock.bind(("172.16.5.222", 30502))
        self.address = address

    def send(self, msg):
        if isinstance(msg, list):
            msgToSend = bytes(msg)
        elif isinstance(msg, bytes):
            msgToSend = msg
        else:
            raise RuntimeError("Invalid data type to send")
        totalsent = 0
        msg_len = len(msg)
        while totalsent < msg_len:
            for _ in range(100):
                sent = self.sock.sendto(msgToSend[totalsent:], self.address)
            if sent == 0:
                raise RuntimeError("TCP socket connection broken")
            totalsent = totalsent + sent

    def close(self):
        time.sleep(1)
        self.sock.close()
