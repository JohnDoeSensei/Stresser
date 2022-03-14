from Socket import Socket
import logging


logging.basicConfig(level=logging.DEBUG)
logging.info('eyo')
s = Socket('udp')
s._connect('192.168.1.10', 1111)
s._send(data='salut')
