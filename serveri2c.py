import smbus2 as smbus
import rpyc
from rpyc.utils.server import ThreadedServer
import sqlite3
import time
import datetime

running_on_pie = False  # pie or windows

conn = sqlite3.connect('order.db')
c = conn.cursor()


def log_it(note):
    if running_on_pie:
        f = open("/home/sysop/pos/server_log.txt", "a+")
    else:
        f = open("server_log.txt", "a+")
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
    info = st + ' > '
    info += note
    info += '\n\r'
    f.write(info)


def data_test(a1):
    c.execute("SELECT * FROM donut WHERE orderNUM=:a1", {"a1": str(a1)})
    data1 = c.fetchall()
    if data1:
        return data1


def data_delete(a1):
    c.execute("DELETE FROM donut WHERE orderNUM=:a1", {"a1": str(a1)})
    conn.commit()


class ServerHead(rpyc.Service):

    def on_connect(self, conn):
        print("connected")

    def on_disconnect(self, conn):
        print("disconnected")


if __name__ == '__main__':
    t = ThreadedServer(ServerHead, port=12345)
    t.start()
