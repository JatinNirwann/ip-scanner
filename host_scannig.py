import threading
from queue import Queue
import netifaces
import time
import os
import scapy.all as scapy

threads =[]

def get_subnet():
    try:
        gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]  #0 for gateway IP
        print(gateway)
        
        return '.'.join(gateway.split('.')[:-1])
        
    except Exception as e:
        print(f"Error getting subnet: {e}")
        return None

subnet = get_subnet()
print(subnet)

def ping_host(ip):
    packet = scapy.IP(dst=ip)/scapy.ICMP()
    reply = scapy.sr1(packet, timeout=1, verbose=False)
    
    if reply:
        print(f"Device found: {ip}")


for i in range(1, 255):
    ip = f"{subnet}.{i}"
    thread = threading.Thread(target=ping_host, args=(ip,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print("Scan complete!")