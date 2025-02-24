import threading
from queue import Queue
import netifaces
import scapy.all as scapy
import time

scapy.conf.verb = 0

def get_subnet():
    try:
        gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
        print(f"Gateway: {gateway}")
        return ".".join(gateway.split(".")[:-1])
    except Exception as e:
        print(f"Error getting subnet: {e}")
        return None

def scan_host(ip):
    try:
        arp_request = scapy.ARP(pdst=ip)
        arp_reply = scapy.srp1(scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / arp_request, timeout=1, verbose=False)

        if arp_reply:
            mac_address = arp_reply.hwsrc  # Get MAC address
            print(f"Device found (ARP): {ip} → MAC: {mac_address}\n")
            return
        time.sleep(0.5)
        arp_reply_retry = scapy.srp1(scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / arp_request, timeout=1, verbose=False)

        if arp_reply_retry:
            mac_address = arp_reply_retry.hwsrc
            print(f"Device found (ARP - Retry): {ip} → MAC: {mac_address}\n")
            return

        packet = scapy.IP(dst=ip) / scapy.ICMP()
        reply = scapy.sr1(packet, timeout=1, verbose=False)

        if reply:
            print(f"Device found (ICMP): {ip} → MAC: Unknown (ICMP-only)\n")

    except Exception as e:
        print(f"Error scanning {ip}: {e}")

def worker():
    while not ip_queue.empty():
        ip = ip_queue.get()
        scan_host(ip)
        ip_queue.task_done()

subnet = get_subnet()
if not subnet:
    print("Failed to get subnet. Exiting...")
    exit()

ip_queue = Queue()

for i in range(1, 255):
    ip_queue.put(f"{subnet}.{i}")

num_threads = 10 
threads = []

for _ in range(num_threads):
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()
    threads.append(thread)

ip_queue.join()

print("Scan complete!")
