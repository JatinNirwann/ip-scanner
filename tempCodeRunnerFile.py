import socket
import threading
from queue import Queue

host_port = 2000
host_found = Queue()
host = input("Enter target ip")

try:
    connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connection.settimeout(0.3)
    connection.connect(host,host_port)
    print("Connection Successfull")
except:
    print("Connection Failed")

finally:
    connection.close()
