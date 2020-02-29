import rpyc
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader

running_on_pie = True  # pie or windows

Window.size = (480, 800)

if running_on_pie:
    host = '192.168.1.10'
else:
    host = '192.168.86.26'

port = 12345

HEADER_LENGTH = 10
window_id = "w1"
not_online = True

sizes = ['None', 'donut', 'donuts']
drinks = ['None', 'Pepsi', 'Mountain Dew', 'Root Beer', '7 Up', 'coffee', 'decaff']


def un_start():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)


class Pick(Widget):

    def __init__(self, **kwargs):
        super(Pick, self).__init__(**kwargs)
        self.numberT = ''
        self.nums = 0
        self.more = False
        self.data = ''
        self.pops = ''
        self.data2 = ''
        self.click = SoundLoader.load('click.wav')
        self.bot = rpyc.connect(host, port=12345)

    def order(self, num):

        if len(self.numberT) <= 3:
            self.numberT += num
            self.ids.number1.text = self.numberT

            if self.click:
                self.click.play()

    def enter_num(self):

        if len(self.numberT) >= 4:
            test1 = self.numberT
            test = self.bot.root.order(self.numberT)
            # test = orders(test1)

            if test1 == '0000':
                un_start()
                # App.get_running_app().stop()
            if test != 'None':
                self.numberT = test
                self.look_at()

            else:
                self.numberT = ''
                self.ids.number1.text = 'XXXX'

    def end_it(self):
        print(self.nums)
        App.get_running_app().stop()

    def clear_num(self):
        self.numberT = ''
        self.data = ''
        self.pops = ''
        self.ids.number1.text = 'XXXX'

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
        self.ids.n_back.pos = 60, 1460
        self.ids.ent.pos = 60, 1460
        self.ids.new.pos = 10, 0
        self.ids.orderT.pos = 175, 120
        self.ids.star.pos = 170, -30

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
            if self.pops[0] == '4':
                self.ids.pop1.pos = 150, 200
            if self.pops[0] == '3':
                self.ids.pop2.pos = 150, 200
            if self.pops[0] == '2':
                self.ids.pop3.pos = 150, 200
            if self.pops[0] == '1':
                self.ids.pop4.pos = 150, 200
        if len(self.pops) > 1:
            # pop number 2
            if self.pops[1] == '4':
                self.ids.pop11.pos = 250, 200
            if self.pops[1] == '3':
                self.ids.pop21.pos = 250, 200
            if self.pops[1] == '2':
                self.ids.pop31.pos = 250, 200
            if self.pops[1] == '1':
                self.ids.pop41.pos = 250, 200
        if len(self.pops) > 2:
            # pop number 3
            if self.pops[2] == '4':
                self.ids.pop12.pos = 350, 200
            if self.pops[2] == '3':
                self.ids.pop22.pos = 350, 200
            if self.pops[2] == '2':
                self.ids.pop32.pos = 350, 200
            if self.pops[2] == '1':
                self.ids.pop42.pos = 350, 200
        if len(self.pops) > 3:
            # pop number 3
            if self.pops[3] == '4':
                self.ids.pop13.pos = 50, 200
            if self.pops[3] == '3':
                self.ids.pop23.pos = 50, 200
            if self.pops[3] == '2':
                self.ids.pop33.pos = 50, 200
            if self.pops[3] == '1':
                self.ids.pop43.pos = 50, 200

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
        self.ids.n0.pos = 155, 35
        self.ids.n1.pos = 10, 435
        self.ids.n2.pos = 155, 435
        self.ids.n3.pos = 300, 435
        self.ids.n4.pos = 10, 300
        self.ids.n5.pos = 155, 300
        self.ids.n6.pos = 300, 300
        self.ids.n7.pos = 10, 170
        self.ids.n8.pos = 155, 170
        self.ids.n9.pos = 300, 170
        self.ids.nc.pos = 325, 60
        self.ids.n_back.pos = 35, 60
        self.ids.ent.pos = 110, 580
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
        # Clock.schedule_interval(self.update, 1)
        print(self.numberT)
        info = self.bot.root.robot(self.numberT)
        print(info)
        if info == 'started':
            self.ids.orderS.text = 'Started.'
        if info == 'end':
            self.reset_all()


class PickApp(App):

    def build(self):
        return Pick()


if __name__ == '__main__':
    PickApp().run()
