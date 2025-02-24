import socket
import threading
from queue import Queue
import netifaces

host_port = 2000
host_found = Queue()

def get_subnet():
    try:
        gateway = netifaces.gateways()['default'][netifaces.AF_INET][1]
        
        addr_info = netifaces.ifaddresses(gateway)[netifaces.AF_INET][0]
        ip_address = addr_info['addr']

        ip_sliced = ip_address.split(".")
        print(ip_sliced)
        final_subnet = ip_sliced[:-1]
        final_subnet_string = '.'.join(final_subnet)
        return f"{final_subnet_string}.0"

    except Exception as e:
        return f"Error: {e}"


subnet = get_subnet()
print(subnet)
try:
    connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connection.settimeout(0.3)
    for i in range(1,256):
        host = subnet + "." + str(i)
    connection.connect((host,host_port))
    print("Connection Successfull")

except:
    print("Connection Failed")

finally:
    connection.close()




