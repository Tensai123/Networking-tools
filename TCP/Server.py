from email.headerregistry import Address
import socket
import threading
import sys

# Collecting data from CLI
bind_ip = str(sys.argv[1])
bind_port = int(sys.argv[2])

# Creating server and starting listening
def main():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    print(f'[*] Listening on {bind_ip}:{bind_port}')
    
    while True:
        client, address = server.accept()
        print(f'[*] Connection accepted  from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

# Handling client connected to server
def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Data received: {request.decode("utf-8")}')
        sock.send(b'ACKKK')

if __name__ == '__main__':
    main()
