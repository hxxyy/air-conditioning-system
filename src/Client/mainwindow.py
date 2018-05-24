from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_KEEPALIVE, socket
from json import loads, dumps
from time import sleep
import sys
import client_ui
from PyQt5.QtWidgets import QApplication, QMainWindow

<<<<<<< HEAD
class Client:
    def __init__(self, rid='1', realtemp=30.0, ulimit=32, llimit=16, swi=0, nowmoney=0.0, adress='10.128.223.55',
                 tport=8080, outtemp=30.0):
        self.roomid = rid
        self.realtimetemperature = realtemp
        self.targettemperature = 26.0
        self.outtemp = outtemp
        self.windVelocity = 0  # 风速1，2
        self.uplimit = ulimit
=======
class client:
    def __init__(self,rid='1',realtemp=30.0,ulimit=32,llimit=16,nowmoney=0.0,adress='127.0.0.1',tport=9008):
        self.clientid=''
        self.roomid=rid
        self.realtimetemperature=realtemp
        self.targettemperature=26.0
        self.windVelocity=0 #风速1，2
        self.uplimit=ulimit
>>>>>>> f637170b8a1050ab1798e0aba27ef637ed0babfa
        self.lowlimit = llimit
        self.money = nowmoney
        self.adress = adress
        self.port = tport
        self.switch = swi

    def interface(self):
        print("now temp:", self.realtimetemperature)
        print("target temp", self.targettemperature)
        print("wind", self.windVelocity)
        print("money", self.money)
        print("id:", self.roomid)

    def changetarget(self, tar):
        if self.lowlimit > tar:
            print("Error! Too Low!")
            return False
        elif self.uplimit < tar:
            print("Error! Too High!")
            return False
        else:
            self.targettemperature = float(tar)
            return True

    def changemodle(self, model):
        self.windVelocity = model
        self.requestreport()

    def sendtcp(self, senddata):
        with socket(AF_INET, SOCK_STREAM) as sc:
            sc.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
            sc.connect((self.adress, self.port))
            send_data = senddata
            sc.sendall(bytes(send_data, encoding="utf8"))
            accept_data = str(sc.recv(1024), encoding="utf8")
            return accept_data

    def temperaturereport(self):
        content = {'type': 1, 'temperature': '%.2f' % self.realtimetemperature, 'room': self.roomid}
        json_str = dumps(content)
        data = self.sendtcp(json_str)
        ans = loads(data)
        self.windVelocity = int(ans['wind'])
        self.money = float(ans['cost'])

    def requestreport(self):
        por = {'type': 0, 'room': self.roomid, 'switch': self.switch, 'temperature': self.realtimetemperature,
               'wind': self.windVelocity}
        json_str = dumps(por)
        self.sendtcp(json_str)

    def changeswitch(self):
        if self.switch == 1:
            self.switch = 0
        else:
            self.switch = 1

    def environmentchange(self):
        if self.switch == 0:
            self.realtimetemperature += (self.outtemp - self.realtimetemperature) * 0.01
        elif self.targettemperature > self.realtimetemperature:
            self.realtimetemperature += round(0.1 * self.windVelocity, 2)
        else:
            self.realtimetemperature -= round(0.1 * self.windVelocity, 2)

    def termtask(self):
        while True:
            sleep(6)
            self.environmentchange()
            self.temperaturereport()

    def edittask(self):
        self.requestreport()
        while True:
            self.interface()
            choice = input("please choice model:1:change temperature,2:change wind,3.changeswitch\n")
            if 1 == int(choice):
                num = input("please imput target\n")
                self.changetarget(int(num))
            elif 2 == int(choice):
                model = input("please input model\n")
                self.changemodle(int(model))
            elif 3 == int(choice):
                self.changeswitch()
            else:
                print("valid input")

<<<<<<< HEAD
if __name__ == "__main__":
    Client1 = Client()
=======

if __name__ == '__main__':
    Client1 = client("2015211301")
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = client_ui.Ui_MainWindow()
    ui.setupUi(MainWindow,Client1)
    MainWindow.show()
    sys.exit(app.exec_())












>>>>>>> f637170b8a1050ab1798e0aba27ef637ed0babfa
