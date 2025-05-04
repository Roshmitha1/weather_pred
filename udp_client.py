# udp_client.py
import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"[CLIENT] Receiving real-time weather updates...\n")

while True:
    data, addr = sock.recvfrom(2048)
    print(f"[RECEIVED] {data.decode()}")


