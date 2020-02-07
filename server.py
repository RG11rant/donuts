import socket
import serial
import sqlite3
import select
import time
import datetime

HEADERSIZE = 10
running_on_pie = False  # pie or windows

if running_on_pie:
    host = '192.168.1.10'
    pos = '192.168.1.10'
    bot = '192.168.1.20'
    win1 = '192.168.1.11'
    win2 = '192.168.1.12'
    conn = sqlite3.connect('/home/sysop/pos/order.db')
else:
    host = '192.168.86.26'
    # host = '127.0.0.1'  # get local machine name
    pos = '192.168.86.26'
    bot = '192.168.86.178'
    win1 = '192.168.86.26'
    win2 = '192.168.86.11'
    conn = sqlite3.connect('order.db')

port = 12345
robot = serial.Serial('COM7', 115200)

c = conn.cursor()

send_to_bot = False
send_to_w1 = False
send_to_w2 = False
send_to_pos = False

bot_data = ''
bot_hold = ''

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((host, port))
serverSocket.listen(5)

sockets_list = [serverSocket]

clients = {}

print('Listening for connections on {}:{}...'.format(host, port))


def un_start():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


def log_it(note):
    if running_on_pie:
        f = open("/home/sysop/pos/log.txt", "a+")
    else:
        f = open("log.txt", "a+")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    info = st + ' > '
    info += note
    info += '\n\r'
    f.write(info)


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS donut(donutID int, drink int, topping int, orderNUM int,'
              ' pay int)')


def data_test(a1):
    c.execute("SELECT * FROM donut WHERE orderNUM=:a1", {"a1": str(a1)})
    data1 = c.fetchall()
    if data1:
        return data1


def data_delete(a1):
    c.execute("DELETE FROM donut WHERE orderNUM=:a1", {"a1": str(a1)})
    conn.commit()


# Handles message receiving
def receive_message(client_socket1):

    try:
        message_header = client_socket1.recv(HEADERSIZE)
        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket1.recv(message_length)}

    except Exception as e:
        print(e)
        return False


def order_process(order):
    if len(order) == 4:
        xa = str(data_test(order))
        if xa != 'None':
            xa = xa.strip('[]()')
            xa = xa.replace(" ", "")
            xa = xa.split(",")
            dm = '$A' + str(xa[0])
            if str(xa[1]) == '0':
                dm += '1000#'
            else:
                dm += str(xa[1])
                dm += '#'
        else:
            dm = xa
        return dm


create_table()


while True:

    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    for notified_socket in read_sockets:
        if notified_socket == serverSocket:
            client_socket, client_address = serverSocket.accept()

            # Client should send his name right away, receive it
            user = receive_message(client_socket)

            # If False - client disconnected before he sent his name
            if user is False:
                continue

            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)

            # Also save username and username header
            clients[client_socket] = user

            print('Accepted connection from {}, username: {}'.format(client_address, user['data'].decode('utf-8')))
            log_it('Accepted connection from {}, username: {}'.format(client_address, user['data'].decode('utf-8')))
        else:
            # Receive message
            message = receive_message(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                log_it('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]
            data = message["data"].decode("utf-8")
            if data != 'ready':
                print('Received message from {}: {}'.format(user["data"].decode("utf-8"), data))
                log_it('Received message from {}: {}'.format(user["data"].decode("utf-8"), data))

            #  main com arduino
            if robot.in_waiting > 0:
                line = robot.readline()
                print(line)

            if user["data"] == 'm1'.encode("utf-8"):
                # start the order
                if data == 'A order In':
                    message2_header = '{:10}'.format(len(data))
                    message['header'] = message2_header.encode("utf-8")
                    message['data'] = data.encode("utf-8")
                    send_to_w1 = True

                if data == 'end':
                    message2_header = '{:10}'.format(len(data))
                    message['header'] = message2_header.encode("utf-8")
                    message['data'] = data.encode("utf-8")
                    send_to_w1 = True

                # cash info from Arduino
                if data[0] == '$':
                    message2_header = '{:10}'.format(len(data))
                    message['header'] = message2_header.encode("utf-8")
                    message['data'] = data.encode("utf-8")
                    send_to_pos = True

                if data == 'ready':
                    bot_data = 'G'
                    send_to_bot = True

            # pos info
            if user["data"] == 'pos'.encode("utf-8"):
                # change to serial com
                print(data)
                bot_data = data
                send_to_bot = True
                # end change

            # window A data and processing
            if user["data"] == 'w1'.encode("utf-8"):
                if len(data) == 4:
                    if data == '0000':
                        un_start()
                    message2 = order_process(data)
                    bot_hold = message2
                    message2_header = '{:10}'.format(len(message2))
                    message['header'] = message2_header.encode("utf-8")
                    message['data'] = message2.encode("utf-8")
                    send_to_w1 = True

                if len(data) == 5:
                    if data == 'start':
                        data = 'end'
                        message2_header = '{:10}'.format(len(data))
                        message['header'] = message2_header.encode("utf-8")
                        message['data'] = data.encode("utf-8")
                        print(bot_data)
                        send_to_bot = True
                        bot_data = bot_hold
                        # send_to_w1 = True

            # Iterate over connected clients and broadcast message
            for client_socket in clients:
                # sent it
                the_ip = client_socket.getpeername()[0]

                if the_ip == win1 and send_to_w1:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                    send_to_w1 = False

                if the_ip == win2 and send_to_w2:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                    send_to_w2 = False

                if the_ip == bot and send_to_bot:
                    client_socket.send(bot_data.encode("utf-8"))
                    send_to_bot = False

                if the_ip == pos and send_to_pos:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
                    send_to_pos = False

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]
