import socket
import threading
from queue import Queue


target_ip = input("Enter the ip address of target device :\n")
no_of_ports = int(input("Enter last port no:\n") or 1025)

difference = int(no_of_ports/4)

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
    for i in range(0,difference):
        if port_scan(i):
            open_ports.put(i)

def scan2():
    for j in range(difference,2*difference):
        if port_scan(j):
            open_ports.put(j)

def scan3():
    for k in range(2*difference,3*difference):
        if port_scan(k):
            open_ports.put(k)
 
def scan4():
    for l in range(3*difference,4*difference):
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