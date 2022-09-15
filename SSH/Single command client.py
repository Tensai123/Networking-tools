from sys import stderr, stdout
import paramiko

def ssh_command(ip, port, user, passwd, cmd):
    client = paramiko.SSHClient()
# Auto accepting ssh key
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

# Executing command on server and displaying result  
    _, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('---Result---')
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    import getpass
    #user = getpass.getuser()
    user = input('Username: ')
    password = getpass.getpass('Password: ')

    ip = input('Server ip address: ')
    port = input('Port: ') or '22'
    cmd = input('Command: ') or 'pwd'
    ssh_command(ip, port, user, password, cmd)