from escpos.printer import Network
import math


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
            epson.text(str(m[0]))
            if int(m[0]) > 1:
                epson.text(' Cups of Donuts')
                price = int(m[0]) * 4.76
                epson.text('     $' + str(price) + '\n')
                price = int(m[0]) * 4.7619
            else:
                epson.text(' Cup of Donuts')
                epson.text('      $4.76\n')
                price = 4.7619

            n = str(m[1])
            if int(n[0]) > 1:
                p = int(n[0]) - 1
                epson.text(str(p) + '  ')
                epson.text('Pepsi')
                p2 = p * 1.9047
                p = p * 1.90
                price = price + p2
                epson.text('             $' + str(p) + '0\n')
            if int(n[1]) > 0:
                epson.text(n[1] + '  ')
                epson.text('Mountain Dew')
                p = int(n[1]) * 1.90
                p2 = int(n[1]) * 1.9047
                price = price + p2
                epson.text('      $' + str(p) + '0\n')
            if int(n[2]) > 0:
                epson.text(n[2] + '  ')
                epson.text('Root Beer')
                p = int(n[1]) * 1.90
                p2 = int(n[1]) * 1.9047
                price = price + p2
                epson.text('         $' + str(p) + '0\n')
            if int(n[3]) > 0:
                epson.text(n[3] + '  ')
                epson.text('7 Up')
                p = int(n[1]) * 1.90
                p2 = int(n[1]) * 1.9047
                price = price + p2
                epson.text('              $' + str(p) + '0\n')

        gst = price * .05
        nice_gst = math.ceil(gst * 100) / 100
        epson.text('               GST:  $' + str(nice_gst) + '\n')
        print(nice_gst)
        price = price + gst
        tot = math.ceil(price * 100) / 100
        epson.text('             Total:  $' + str(tot) + '0\n')
        print(tot)
        epson.text('\n\n')
        epson.set(font='a', height=2, width=2, align='center')
        epson.text('THANK YOU\n')
        epson.set(font='a', height=1, width=1, align='center')
        epson.barcode(bar, 'CODE128', function_type="B")
        epson.cut()
    except Exception as ex:
        print(ex)


order_in = [[2, 2101, 0, 8819, 1]]

pos_print(order_in)
