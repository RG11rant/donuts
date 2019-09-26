import socket
import sys
import errno

running_on = 'pi'  # pie or windows

if running_on == 'pie':
    host = '192.168.1.10'
else:
    host = '192.168.86.26'


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 12345
window_id = "pos"

HEADER_LENGTH = 10

try:
    print('starting host.')
    client_socket.connect((host, port))  # uncomment on raspberry pi
    client_socket.setblocking(False)

    username = window_id.encode('utf-8')
    username_header = '{:10}'.format(len(username)).encode('utf-8')
    client_socket.send(username_header + username)
    print("connected")
except Exception as e:
    print(e)


def messages():
    try:
        window_header = client_socket.recv(HEADER_LENGTH)
        if not len(window_header):
            print('Connection closed by the server')
            sys.exit()

        username_length = int(username_header.decode('utf-8').strip())
        username1 = client_socket.recv(username_length).decode('utf-8')
        if username1 == 'me':
            print(username1)

        message_header = client_socket.recv(9)
        message_length = int(message_header.decode('utf-8').strip())
        message = client_socket.recv(message_length).decode('utf-8')
        return message

    except IOError as et:
        if et.errno != errno.EAGAIN and et.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(et)))
            sys.exit()

    except Exception as em:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(em)))
        # sys.exit()



def un_start():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

