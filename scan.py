import socket
import threading
from queue import Queue

target_ip = "192.168.1.8"
def port_scan(port):
    print(f"Scanning {port}")
    try:
        sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((target_ip ,port))
        sock.close()
        open_ports.put(port)
        return True
    except:
        return False
    
open_ports= Queue()
threading_queue = Queue()




def scan1():
    for i in range(1,31):
        if port_scan(i):
            open_ports.put(i)

def scan2():
    for j in range(31,51):
        if port_scan(j):
            open_ports.put(j)

def scan3():
    for k in range(51,71):
        if port_scan(k):
            open_ports.put(k)
 
def scan4():
    for l in range(71,91):
        if port_scan(l):
            open_ports.put(l)

first_thread =threading.Thread(target=scan1)
second_thread = threading.Thread(target=scan2)
third_thread =threading.Thread(target=scan3)
forth_thread = threading.Thread(target=scan4)

first_thread.start()
second_thread.start()
third_thread.start()
forth_thread.start()

first_thread.join()
second_thread.join()
third_thread.join()
forth_thread.join()


open_ports_list = list(open_ports.queue)

if open_ports_list:
    print(f"Open ports on {target_ip}: {open_ports_list}")
else:
    print(f"No open ports found on {target_ip}")