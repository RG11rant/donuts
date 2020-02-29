import rpyc
from rpyc.utils.server import ThreadedServer
import sqlite3
import time
import datetime
import serial

running_on_pie = False   # pie or windows

if running_on_pie:
    conn = sqlite3.connect('/home/sysop/pos/order.db', check_same_thread=False)
    robot = serial.Serial('/dev/ttyUSB0', 19200, timeout=None)
else:
    conn = sqlite3.connect('order.db', check_same_thread=False)
    robot = serial.Serial('COM9', 19200, timeout=None)

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


class ServerHead(rpyc.Service):
    def __init__(self, **kwargs):
        super(ServerHead, self).__init__(**kwargs)
        self.bill = False
        self.phil = False  # remove
        self.last = ''
        self.onbord = 0

    def on_connect(self, connects):
        self.onbord += 1
        print("connected")

    def on_disconnect(self, connects):
        self.onbord -= 1
        print("disconnected")

    @staticmethod
    def exposed_order(orders):
        message = order_process(orders)
        log_it(message)
        return message

    def exposed_robot(self, bot):
        while self.bill:
            time.sleep(.5)
        self.bill = True
        robot.write(bot.encode("utf-8"))
        line_in = robot.readline()
        line = line_in.decode("utf-8")
        line = line.rstrip()
        log_it(line)
        print(line)
        self.bill = False
        return line

    def exposed_pay(self, bot):
        while self.bill:
            time.sleep(.25)
        self.bill = True
        robot.write(bot.encode("utf-8"))
        line_in = robot.readline()
        line = line_in.decode("utf-8")
        line = line.rstrip()
        if line != self.last:
            print(line)
            log_it(line)
            self.last = line
        self.bill = False
        return line

    def exposed_card(self):
        while self.phil:
            time.sleep(.25)
        self.bill = True
        sender = 'C#'
        robot.write(sender.encode("utf-8"))
        line_in = robot.readline()
        line = line_in.decode("utf-8")
        line = line.rstrip()
        self.bill = False
        return line


if __name__ == '__main__':
    t = ThreadedServer(ServerHead, port=12345)
    print(t.host)
    t.start()
