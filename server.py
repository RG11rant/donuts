import socket
import sqlite3

conn = sqlite3.connect('order.db')
c = conn.cursor()
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# get local machine name
host = '127.0.0.1'
port = 12345
# bind to the port
serverSocket.bind((host, port))
serverSocket.listen(5)
print('holding for connection')
clientSocket, address = serverSocket.accept()
print("Got a connection from %s" % str(address))


sizes = ['None', 'donut', 'donuts']
drinks = ['None', 'Pepsi', 'Mountain Dew', 'Root Beer', '7 Up', 'coffee', 'decaff']


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS donut(donutID int, drink int, topping int, orderNUM int,'
              ' pay int)')


def data_test(a1):
    c.execute("SELECT * FROM donut WHERE orderNUM=:a1", {"a1": str(a1)})
    data = c.fetchall()
    if data:
        return data


def data_delete(a1):
    c.execute("DELETE FROM donut WHERE orderNUM=:a1", {"a1": str(a1)})
    conn.commit()


create_table()


while True:
    data = clientSocket.recv(1024).decode('utf-8')
    if not data:
        break

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
    clientSocket.send(d.encode('utf-8'))

c.close()
conn.close()
clientSocket.close()
