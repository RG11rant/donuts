import socket
import sqlite3
import time
import select

conn = sqlite3.connect('order.db')
c = conn.cursor()

HEADERSIZE = 10

# host = '192.168.1.6'
host = '127.0.0.1'  # get local machine name
port = 12345

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serverSocket.bind((host, port))
serverSocket.listen(5)

sockets_list = [serverSocket]

clients = {}

print(f'Listening for connections on {host}:{port}...')

sizes = ['None', 'donut', 'donuts']
drinks = ['None', 'Pepsi', 'Mountain Dew', 'Root Beer', '7 Up', 'coffee', 'decaff']


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

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address,
                                                                            user['data'].decode('utf-8')))
        else:
            # Receive message
            message = receive_message(notified_socket)

            # If False, client disconnected, cleanup
            if message is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))

                # Remove from list for socket.socket()
                sockets_list.remove(notified_socket)

                # Remove from our list of users
                del clients[notified_socket]

                continue

            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]

            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            data = message["data"].decode("utf-8")
            if len(data) == 4:
                x = str(data_test(data))
                if x != 'None':
                    x = x.strip('[]')
                    x = x.strip('()')
                    x = x.replace(" ", "")
                    x = x.split(",")
                    d = '$'
                    d += 'A'
                    d += str(x[0])
                    if str(x[1]) == '0':
                        d += '1000'
                    else:
                        d += str(x[1])
                        d += '#'
                else:
                    d = x
                print(d)
                message2 = d
                message2_header = f"{len(message2):<{HEADERSIZE}}"
                message['header'] = message2_header.encode("utf-8")
                message['data'] = message2.encode("utf-8")

            # Iterate over connected clients and broadcast message
            for client_socket in clients:
                # But don't sent it to sender
                if client_socket == notified_socket:
                    print(user['header'] + user['data'] + message['header'] + message['data'])
                    # Send user and message (both with their headers)
                    # We are reusing here message header sent by sender, and saved username
                    # header send by user when he connected
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del clients[notified_socket]


    # old stuff
#     data = clientSocket.recv(1024).decode('utf-8')
#     if not data:
#        break
#     if len(data) == 5:
#         x = str(data_test(data))
#         if x != 'None':
#             x = x.strip('[]')
#             x = x.strip('()')
#             x = x.replace(" ", "")
#             x = x.split(",")
#             d = '$'
#             d += 'A'
#             d += str(x[0])
#             if str(x[1]) == '0':
#                 d += '1000'
#             else:
#                 d += str(x[1])
#             d += '#'
#         else:
#             d = x
#         print(d)
#         clientSocket.send(d.encode('utf-8'))
#     else:
#         print("start123")
#         db = 'started'
#         clientSocket.send(db.encode('utf-8'))
#         time.sleep(3)
#         print('end')
#         db = 'end'
#         clientSocket.send(db.encode('utf-8'))
#
# c.close()
# conn.close()
# clientSocket.close()
