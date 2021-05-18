import sqlite3
import socket
import time
import random
import math
import errno
import sys
import datetime
from escpos.printer import Network
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock


running_on = 'pie'  # pie or windows

if running_on == 'pie':
    host = '192.168.1.10'
    conn = sqlite3.connect('/home/sysop/pos/order.db')
else:
    host = '192.168.86.26'
    Window.size = (1280, 768)
    conn = sqlite3.connect('order.db')

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 12345
window_id = "pos"

HEADER_LENGTH = 10

try:
    print('starting host.')
    client_socket.connect((host, port))  # uncomment on raspberry pi
    client_socket.setblocking(True)

    username = window_id.encode('utf-8')
    username_header = '{:10}'.format(len(username)).encode('utf-8')
    client_socket.send(username_header + username)
    print("connected")
except Exception as e:
    print(e)

c = conn.cursor()

drinks = ['None', 'Pepsi', 'Mountain Dew', 'Root Beer', '7 Up', 'coffee', 'decaff']


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS donut(donutID int, drink int, topping int, orderNUM int,'
              ' pay int, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')


def data_entry(a1, b1, c1, d1, e1):
    c.execute("INSERT INTO donut(donutID, drink, topping, orderNUM, pay) VALUES(?, ?, ?, ?, ?)",
              (a1, b1, c1, d1, e1))
    conn.commit()


def data_test():
    while True:
        a1 = random.randrange(1000, 9999)
        c.execute("SELECT * FROM donut WHERE orderNUM=:a1", {"a1": str(a1)})
        data = c.fetchall()
        if not data:
            return a1
        else:
            print('looking....')


def donut_que(data):
    try:
        message = data.encode('utf-8')
        message_header = '{:10}'.format(len(message)).encode('utf-8')
        client_socket.send(message_header + message)
    except Exception as ex:
        print(ex)
    time.sleep(1)


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
        message_header = client_socket.recv(10)
        print(message_header)
        message_length = int(message_header.decode('utf-8').strip())
        message = client_socket.recv(message_length).decode('utf-8')
        print(message)
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


def pos_print(order=None):
    if order is None:
        order = []
    try:
        epson = Network("192.168.1.100")
        epson.image("/home/sysop/pos/rosie.png")
        bar = '0000'
        price = 0
        for m in order:
            epson.set(height=2, width=2, align='center')
            epson.text('Your PIN\n')
            epson.set(font='a', height=3, width=3, align='center')
            epson.text(str(m[3]) + '\n')
            bar = str(m[3])
            epson.set(font='a', height=2, width=2, align='left', text_type='u2')
            epson.text('    Order   \n')
            epson.set(text_type='normal')

            if int(m[0]) > 1:
                epson.text(str(m[0]))
                epson.text(' Cups of Donuts')
                price = int(m[0]) * 4.76
                epson.text('     $' + str(price) + '\n')
                price = int(m[0]) * 4.7619
            elif int(m[0]) == 1:
                epson.text(str(m[0]))
                epson.text(' Cup of Donuts')
                epson.text('      $4.76\n')
                price = 4.7619

            n = str(m[1])
            if len(n) > 2:
                if int(n[0]) > 1:
                    p = int(n[0]) - 1
                    epson.text(str(p) + '  ')
                    epson.text('Mountain Dew')
                    p2 = p * 1.9047
                    p = p * 1.90
                    p = math.ceil(p * 100) / 100
                    price = price + p2
                    epson.text('      $' + str(p) + '0\n')
                if int(n[1]) > 0:
                    epson.text(n[1] + '  ')
                    epson.text('Root Beer')
                    p = int(n[1]) * 1.90
                    p2 = int(n[1]) * 1.9047
                    p = math.ceil(p * 100) / 100
                    price = price + p2
                    epson.text('         $' + str(p) + '0\n')
                if int(n[2]) > 0:
                    epson.text(n[2] + '  ')
                    epson.text('7 Up')
                    p = int(n[2]) * 1.90
                    p2 = int(n[2]) * 1.9047
                    p = math.ceil(p * 100) / 100
                    price = price + p2
                    epson.text('              $' + str(p) + '0\n')
                if int(n[3]) > 0:
                    epson.text(n[3] + '  ')
                    epson.text('Pepsi')
                    p = int(n[3]) * 1.90
                    p2 = int(n[3]) * 1.9047
                    p = math.ceil(p * 100) / 100
                    price = price + p2
                    epson.text('             $' + str(p) + '0\n')

        gst = price * .05
        nice_gst = math.ceil(gst * 100) / 100
        if len(str(nice_gst)) < 4:
            epson.text('               GST:  $' + str(nice_gst) + '0\n')
        else:
            epson.text('               GST:  $' + str(nice_gst) + '\n')
        price = price + gst
        tot = math.ceil(price * 100) / 100
        epson.text('             Total:  $' + str(tot) + '0\n')
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y %H:%M:%S')
        epson.set(font='a', height=1, width=1, align='center')
        epson.text(st)
        epson.text('\n\n')
        epson.set(font='a', height=2, width=2, align='center')
        epson.text('THANK YOU\n')
        epson.set(font='a', height=1, width=1, align='center')
        epson.barcode(bar, 'CODE128', function_type="B")
        epson.cut()
    except Exception as ex:
        print(ex)


class Pos(Widget):

    def __init__(self, **kwargs):
        super(Pos, self).__init__(**kwargs)
        self.cash = 0.00
        self.gst = 0.00
        self.total = 0.00
        self.key_num = 0
        self.drink_num = 1000
        self.pop_index = 0
        self.m = 0
        self.money = "0"
        self.call_me = 0
        self.pop_name = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.num = [0, 0, 0, 0, 0]
        self.order = []
        if running_on == 'pie':
            self.click = SoundLoader.load('/home/sysop/pos/sound/blip.wav')
        else:
            self.click = SoundLoader.load('sound/blip.wav')

    def clear_it(self):
        self.cash = 0.00
        self.gst = 0.00
        self.ids.Gst1.text = '$0.00'
        self.ids.Cash1.text = '$0.00'
        self.ids.order1S.text = ''
        self.ids.order1SZP.text = ''
        self.ids.pops1.text = ''
        self.ids.pop_price1.text = ''
        self.ids.pops2.text = ''
        self.ids.pop_price2.text = ''
        self.ids.pops3.text = ''
        self.ids.pop_price3.text = ''
        self.ids.pops4.text = ''
        self.ids.pop_price4.text = ''
        self.ids.donut_price1.pos = 5500, 470
        self.ids.donut_price2.pos = 5500, 470
        self.ids.donut_price3.pos = 5500, 470
        self.ids.donut_price4.pos = 5500, 470
        self.ids.soup4.pos = 5500, 470
        self.ids.soup1.pos = 5500, 320
        self.ids.soup2.pos = 5500, 170
        self.ids.soup3.pos = 5500, 20
        self.ids.drink.pos = 1100, 3000
        self.ids.pop1.pos = 500, 3000
        self.ids.pop2.pos = 700, 3000
        self.ids.pop3.pos = 900, 3000
        self.ids.pop4.pos = 1100, 3000
        self.ids.done.pos = 550, 3000

    def set_num(self):
        self.key_num = data_test()

    def starts(self):
        self.ids.star.pos = 5500, 150
        self.ids.soup1.pos = 500, 360
        self.ids.soup2.pos = 900, 360
        self.ids.soup3.pos = 500, 20
        self.ids.soup4.pos = 900, 20
        self.ids.donut_price1.pos = 600, 400
        self.ids.donut_price2.pos = 1000, 400
        self.ids.donut_price3.pos = 600, 80
        self.ids.donut_price4.pos = 1000, 80
        self.ids.new.pos = 40, -10
        self.ids.drink.pos = 200, -10
        if self.click:
            self.click.play()
        self.num[3] = self.key_num

    def soup(self, x):
        if self.click:
            self.click.play()
        if x == '1':
            self.ids.order1S.text = '1 Bag of donuts'
            self.ids.order1SZP.text = '$4.76'
            self.cash += 4.7619
        if x == '2':
            self.ids.order1S.text = '2 Bags of donuts'
            self.ids.order1SZP.text = '$9.52'
            self.cash += 9.52
        if x == '3':
            self.ids.order1S.text = '3 Bags of donuts'
            self.ids.order1SZP.text = '$14.28'
            self.cash += 14.28
        if x == '4':
            self.ids.order1S.text = '4 Bags of donuts'
            self.ids.order1SZP.text = '$19.04'
            self.cash += 19.04

        self.num[0] = int(x)
        self.ids.donut_price1.pos = 5500, 470
        self.ids.donut_price2.pos = 5500, 470
        self.ids.donut_price3.pos = 5500, 470
        self.ids.donut_price4.pos = 5500, 470
        self.ids.soup4.pos = 5500, 470
        self.ids.soup1.pos = 5500, 320
        self.ids.soup2.pos = 5500, 170
        self.ids.soup3.pos = 5500, 20
        self.ids.drink.pos = 1100, 3000
        # move in the pop.
        self.ids.pop1.pos = 500, 300
        self.ids.pop2.pos = 700, 300
        self.ids.pop3.pos = 900, 300
        self.ids.pop4.pos = 1100, 300
        self.ids.done.pos = 550, 50
        # cash math
        self.gst = self.cash * .05
        sg = math.ceil(self.gst * 100) / 100
        sub = '$' + str(sg)
        self.ids.Gst1.text = sub
        tot1 = self.cash + self.gst
        tot2 = math.ceil(tot1 * 100) / 100
        self.total = tot2
        tots = '$' + str(tot2) + '0'
        self.ids.Cash1.text = tots

    def sizes(self, x):
        pass

    def side(self, x):
        pass

    def pop(self, x):
        if self.click:
            self.click.play()
        if x == '1':
            self.pop_name[self.pop_index] = 'Pepsi'
            self.pop_name[self.pop_index + 4] = '$1.90'
            self.drink_num += 1
        if x == '2':
            self.pop_name[self.pop_index] = '7up'
            self.pop_name[self.pop_index + 4] = '$1.90'
            self.drink_num += 10
        if x == '3':
            self.pop_name[self.pop_index] = 'Root Beer'
            self.pop_name[self.pop_index + 4] = '$1.90'
            self.drink_num += 100
        if x == '4':
            self.pop_name[self.pop_index] = 'Mountain Dew'
            self.pop_name[self.pop_index + 4] = '$1.90'
            self.drink_num += 1000
        self.ids.pops1.text = self.pop_name[0]
        self.ids.pop_price1.text = self.pop_name[4]
        self.ids.pops2.text = self.pop_name[1]
        self.ids.pop_price2.text = self.pop_name[5]
        self.ids.pops3.text = self.pop_name[2]
        self.ids.pop_price3.text = self.pop_name[6]
        self.ids.pops4.text = self.pop_name[3]
        self.ids.pop_price4.text = self.pop_name[7]
        self.pop_index += 1
        # end pop display
        self.num[1] = int(self.drink_num)
        self.num[4] = 0
        self.num[3] = self.key_num
        self.cash += 1.9047
        self.gst = self.cash * .05
        sg = math.ceil(self.gst * 100) / 100
        sub = '$' + str(sg)
        self.ids.Gst1.text = sub
        tot1 = self.cash + self.gst
        tot2 = math.ceil(tot1 * 100) / 100
        self.total = tot2
        tots = '$' + str(tot2) + '0'
        self.ids.Cash1.text = tots
        if self.pop_index > 3:
            self.ids.pop1.pos = 500, 3000
            self.ids.pop2.pos = 700, 3000
            self.ids.pop3.pos = 900, 3000
            self.ids.pop4.pos = 1100, 3000
            self.ids.done.pos = 550, 3000
            self.ids.pay.pos = 550, 400

    def pops(self):
        self.ids.pop1.pos = 500, 3000
        self.ids.pop2.pos = 700, 3000
        self.ids.pop3.pos = 900, 3000
        self.ids.pop4.pos = 1100, 3000
        self.ids.done.pos = 550, 3000
        self.ids.pay.pos = 550, 400

    def pay(self):
        self.m = 1
        self.ids.pay.pos = 5500, 400
        bills = '%'
        bills += str(self.total * 4)
        bills += '#'
        self.money = bills
        # donut_que(bills)
        self.ids.bill.pos = 800, 300
        self.ids.bill_name.pos = 800, 400
        self.ids.payed.pos = 1000, 500
        self.ids.payed_name.pos = 700, 500
        self.ids.changes.pos = 800, 100
        self.ids.paid.pos = 1000, 0
        sub = '$' + str(self.total)
        self.ids.payed.text = sub
        self.ids.bill.text = '0.00'
        self.ids.changes.text = ''
        Clock.schedule_interval(self.update, 3)

    def update(self, _):
        donut_que(self.money)
        self.m += 1
        bill_it = self.total
        info = messages()
        print(info)
        if 900 > self.m > 3:
            if info is not None:
                if info[0] == '$':
                    paying = info.strip('$')
                    paying = int(paying)
                    paying = paying / 4
                    total = bill_it - paying
                    total_s = '$'
                    total_s += str(total)
                    if paying > 0:
                        info = '$'
                        info += str(paying)
                        change = ' '

                    else:
                        change = '$'
                        change += str(abs(paying))
                        self.ids.changes_name.pos = 800, 200
                        info = 'Payed'
                        self.m = 890

                    self.ids.payed.text = info
                    self.ids.bill.text = total_s
                    self.ids.changes.text = change

        elif self.m > 900:
            donut_que('F')
            self.payed()
            Clock.unschedule(self.update)

    def payed(self):
        Clock.unschedule(self.update)
        self.ids.bill.pos = 7000, 500
        self.ids.bill_name.pos = 8000, 400
        self.ids.payed.pos = 7000, 500
        self.ids.payed_name.pos = 7000, 500
        self.ids.changes.pos = 7000, 500
        self.ids.changes_name.pos = 8000, 200
        self.ids.new.pos = 900, 3000
        self.ids.paid.pos = 700, 3000
        self.num[4] = 1
        self.order.append(self.num)
        self.drink_num = 1000
        self.cash = 0.00
        self.gst = 0.00
        self.total = 0.00
        self.ids.Gst1.text = '$0.00'
        self.ids.Cash1.text = '$0.00'
        m = 'D'
        for x in self.order:
            data_entry(x[0], x[1], x[2], x[3], x[4])
            n = x[3]
            y = str(x)
            y = y.strip('[]')
            print(y)
            m += y[0]
            print(n)
        m += '#'
        print(m)
        if running_on == 'pie':
            pos_print(self.order)

        donut_que(str(m))
        self.pop_name = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.num = [0, 0, 0, 0, 0]
        self.pop_index = 0
        del self.order[:]
        self.clear_it()
        self.ids.star.pos = 550, 150

    def next(self):
        self.ids.pay.pos = 900, 3000
        self.ids.new.pos = 900, 3000
        del self.order[:]
        self.num = [0, 0, 0, 0, 0]
        self.pop_name = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.pop_index = 0
        self.drink_num = 1000
        self.clear_it()
        # if running_on == 'pie':
        #    un_start()
        # App.get_running_app().stop()
        self.ids.star.pos = 550, 150

    def done(self):
        self.pop_index = 0
        if running_on == 'pie':
            un_start()
        App.get_running_app().stop()


create_table()


class PosApp(App):

    def build(self):
        return Pos()


if __name__ == '__main__':
    PosApp().run()
