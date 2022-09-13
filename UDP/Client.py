import socket
import sys

#Collecting data from CLI
target_host = str(sys.argv[1])
target_port = int(sys.argv[2])
data_to_send = str(sys.argv[3])

#Creating socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Sending data
client.sendto(data_to_send.encode(), (target_host,target_port))

#Receiving data
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()
