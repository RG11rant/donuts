from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
import socket
import time

Window.size = (480, 800)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'  # get local machine name
port = 12345

try:
    sock.connect((host, port))
except Exception as e:
    print(e)

sizes = ['None', 'donut', 'donuts']
drinks = ['None', 'Pepsi', 'Mountain Dew', 'Root Beer', '7 Up', 'coffee', 'decaff']


def robot(data):
    try:
        data += '\n'
        sock.send(data.encode('utf-8'))
    except Exception as ex:
        print(ex)
    time.sleep(1)


def messages():
    try:
        sock.settimeout(.1)
        bill = sock.recv(1024)
        return bill.decode('utf-8')
    except Exception as ex:
        if ex == 'timed out':
            return 'waiting'


class Pick(Widget):

    def __init__(self, **kwargs):
        super(Pick, self).__init__(**kwargs)
        self.numberT = ''
        self.nums = 0
        self.more = False
        self.data = ''
        self.pops = ''
        self.data2 = ''

    def order(self, num):
        self.numberT += num
        self.ids.number1.text = self.numberT
        if len(self.numberT) >= 4:
            test1 = self.numberT
            robot(test1)
            test = messages()
            print(test)
            if test1 == '0389':
                print('starting')
            if test1 == '0000':
                App.get_running_app().stop()
            if test1 == '0338':
                print("more")
                self.more = True
            if test != "None":
                self.numberT = test
                self.look_at()
            else:
                if not self.more:
                    self.numberT = ''
                    self.ids.number1.text = self.numberT

    def end_it(self):
        print(self.nums)
        sock.close()
        App.get_running_app().stop()

    def clear_num(self):
        self.numberT = ''
        self.data = ''
        self.pops = ''
        self.ids.number1.text = self.numberT

    def look_at(self):
        self.ids.n0.pos = 60, 1460
        self.ids.n1.pos = 60, 1460
        self.ids.n2.pos = 60, 1460
        self.ids.n3.pos = 60, 1460
        self.ids.n4.pos = 60, 1460
        self.ids.n5.pos = 60, 1460
        self.ids.n6.pos = 60, 1460
        self.ids.n7.pos = 60, 1460
        self.ids.n8.pos = 60, 1460
        self.ids.n9.pos = 60, 1460
        self.ids.nc.pos = 60, 1460
        self.ids.new.pos = 10, 0
        self.ids.orderT.pos = 175, 120
        self.ids.star.pos = 170, -30
        # self.numberT = data_test(self.nums)

        self.data = self.numberT
        if self.data[2] == '1':
            self.ids.do1.pos = 80, 400
        if self.data[2] == '2':
            self.ids.do2.pos = 80, 400
        if self.data[2] == '3':
            self.ids.do3.pos = 80, 400
        if self.data[2] == '4':
            self.ids.do4.pos = 80, 400
        for m in range(0, int(self.data[3]) - 1):
            self.pops += '1'
        for m in range(0, int(self.data[4])):
            self.pops += '2'
        for m in range(0, int(self.data[5])):
            self.pops += '3'
        for m in range(0, int(self.data[6])):
            self.pops += '4'
        if len(self.pops) > 0:
            # pop number 1
            if self.pops[0] == '1':
                self.ids.pop1.pos = 50, 200
            if self.pops[0] == '2':
                self.ids.pop2.pos = 50, 200
            if self.pops[0] == '3':
                self.ids.pop3.pos = 50, 200
            if self.pops[0] == '4':
                self.ids.pop4.pos = 50, 200
        if len(self.pops) > 1:
            # pop number 2
            if self.pops[1] == '1':
                self.ids.pop11.pos = 150, 200
            if self.pops[1] == '2':
                self.ids.pop21.pos = 150, 200
            if self.pops[1] == '3':
                self.ids.pop31.pos = 150, 200
            if self.pops[1] == '4':
                self.ids.pop41.pos = 150, 200
        if len(self.pops) > 2:
            # pop number 3
            if self.pops[2] == '1':
                self.ids.pop12.pos = 250, 200
            if self.pops[2] == '2':
                self.ids.pop22.pos = 250, 200
            if self.pops[2] == '3':
                self.ids.pop32.pos = 250, 200
            if self.pops[2] == '4':
                self.ids.pop42.pos = 250, 200
        if len(self.pops) > 3:
            # pop number 3
            if self.pops[3] == '1':
                self.ids.pop13.pos = 350, 200
            if self.pops[3] == '2':
                self.ids.pop23.pos = 350, 200
            if self.pops[3] == '3':
                self.ids.pop33.pos = 350, 200
            if self.pops[3] == '4':
                self.ids.pop43.pos = 350, 200

    def reset_all(self):
        # move out
        self.ids.do1.pos = 80, 4000
        self.ids.do2.pos = 80, 4000
        self.ids.do3.pos = 80, 4000
        self.ids.do4.pos = 80, 4000
        self.ids.pop1.pos = 50, 2000
        self.ids.pop2.pos = 50, 2000
        self.ids.pop3.pos = 50, 2000
        self.ids.pop4.pos = 50, 2000
        self.ids.pop11.pos = 150, 2000
        self.ids.pop21.pos = 150, 2000
        self.ids.pop31.pos = 150, 2000
        self.ids.pop41.pos = 150, 2000
        self.ids.pop12.pos = 250, 2000
        self.ids.pop22.pos = 250, 2000
        self.ids.pop32.pos = 250, 2000
        self.ids.pop42.pos = 250, 2000
        self.ids.pop13.pos = 350, 2000
        self.ids.pop23.pos = 350, 2000
        self.ids.pop33.pos = 350, 2000
        self.ids.pop43.pos = 350, 2000
        self.ids.new.pos = 0, 1000
        self.ids.orderT.pos = 175, 1200
        self.ids.star.pos = 180, -3000
        self.ids.orderS.pos = 175, 6000
        # move in
        self.ids.n0.pos = 180, 100
        self.ids.n1.pos = 60, 460
        self.ids.n2.pos = 180, 460
        self.ids.n3.pos = 300, 460
        self.ids.n4.pos = 60, 340
        self.ids.n5.pos = 180, 340
        self.ids.n6.pos = 300, 340
        self.ids.n7.pos = 60, 220
        self.ids.n8.pos = 180, 220
        self.ids.n9.pos = 300, 220
        self.ids.nc.pos = 300, 100
        self.clear_num()

    def starting(self):
        self.ids.do1.pos = 80, 4000
        self.ids.do2.pos = 80, 4000
        self.ids.do3.pos = 80, 4000
        self.ids.do4.pos = 80, 4000
        self.ids.pop1.pos = 50, 2000
        self.ids.pop2.pos = 50, 2000
        self.ids.pop3.pos = 50, 2000
        self.ids.pop4.pos = 50, 2000
        self.ids.pop11.pos = 150, 2000
        self.ids.pop21.pos = 150, 2000
        self.ids.pop31.pos = 150, 2000
        self.ids.pop41.pos = 150, 2000
        self.ids.pop12.pos = 250, 2000
        self.ids.pop22.pos = 250, 2000
        self.ids.pop32.pos = 250, 2000
        self.ids.pop42.pos = 250, 2000
        self.ids.pop13.pos = 350, 2000
        self.ids.pop23.pos = 350, 2000
        self.ids.pop33.pos = 350, 2000
        self.ids.pop43.pos = 350, 2000
        self.ids.new.pos = 0, 1000
        self.ids.orderT.pos = 175, 1200
        self.ids.star.pos = 180, -3000
        self.ids.orderS.pos = 175, 600
        Clock.schedule_interval(self.update, 1)
        robot('start it')
        print('yes')

    def update(self, dt):
        info = messages()
        if info:
            print(info)
        if info == 'started':
            self.ids.orderS.text = 'Started.'
        if info == 'end':
            print(dt)
            Clock.unschedule(self.update)
            self.reset_all()


class PickApp(App):

    def build(self):
        return Pick()


if __name__ == '__main__':
    PickApp().run()
