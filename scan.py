import socket
import threading
from queue import Queue

target_ip = "192.168.1.8"
def port_scan(port):
    print(f"Scanning {port}")
    try:
        sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((target_ip ,port))
        sock.close()
        
        return True
    except:
        return False
    
open_ports=[]
threading_queue = Queue()

for i in range(81):
    if port_scan(i):
        open_ports.append(i)

    
count=len(open_ports)
if count>0:
    print(open_ports)
else:
    print(f"no open port found on {target_ip}")


