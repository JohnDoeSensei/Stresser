from asyncio.log import logger
import socket
import os



ALLOW_TYPE = ['udp','tcp','syn']

class Socket :
    def __init__(self, type, id): 
        try : 
            if type in ALLOW_TYPE :
                if type == 'udp':
                    self.socket = self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.status = 0
            self.packet_send = 0
            self.id = id
        
        except Exception as e :
            print(e)

    def _connect(self, target, port:int):
        self.socket.connect((target, port))
        self.status = 1
        return 0

    def _send(self, size=65335, data=None):
        assert self.status == 1, 'Socket must be connected before send any bytes'
        if data is None :
                data = os.urandom(size)
                self.socket.send(data)
                self.packet_send += 1
                if self.packet_send % 10 == 0 :
                    print('socket ',self.id, ' : ', self.packet_send)
                
        if isinstance(data, str) :
            while True: 
                data = bytes(data.encode('utf-8'))
                self.socket.send(data)


