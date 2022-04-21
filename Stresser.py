import uuid
import socket

class Stresser(object)  :
    def __init__(self, duration:int, threads:int) -> None:
        self.id = uuid.uuid4()
        self.packet_sent = 0
        self.duration = duration
        self.threads = threads

    def get_ip(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
