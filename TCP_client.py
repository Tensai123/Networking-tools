import socket
import sys

target_host = str(sys.argv[1])
target_port = int(sys.argv[2])
data_to_send = (open(sys.argv[3]).read()+"\r\n\r\n")

#Creating socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connecting with socket
client.connect((target_host, target_port))

#Sending data
client.send(data_to_send.encode())

#Receiving data 
response = client.recv(4096)
print(response.decode())
client.close()
