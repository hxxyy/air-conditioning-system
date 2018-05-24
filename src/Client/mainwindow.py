import socket
from json import loads,dumps
from time import sleep
import sys
import client_ui
from PyQt5.QtWidgets import QApplication, QMainWindow

class client:
    def __init__(self,rid='1',realtemp=30.0,ulimit=32,llimit=16,nowmoney=0.0,adress='127.0.0.1',tport=9008):
        self.clientid=''
        self.roomid=rid
        self.realtimetemperature=realtemp
        self.targettemperature=26.0
        self.windVelocity=0 #风速1，2
        self.uplimit=ulimit
        self.lowlimit = llimit
        self.money=nowmoney
        self.adress=adress
        self.port=tport

    def interface(self):
        print("now temp:",self.realtimetemperature)
        print("target temp",self.targettemperature)
        print("wind",self.windVelocity)
        print("money",self.money)
        print("id:",self.roomid)

    def changetarget(self,tar):
        if self.lowlimit>tar:
            print("Error! Too Low!")
            return False
        elif self.uplimit<tar:
            print("Error! Too High!")
            return False
        else:
            self.targettemperature = float(tar)
            return True

    def changemodle(self,model):
        self.windVelocity=model


    def sendtcp(self,senddata):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            s.connect((self.adress, self.port))
            send_data=senddata
            s.sendall(bytes(send_data, encoding="utf8"))
    def receivetcp(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

            accept_data = str(s.recv(1024), encoding="utf8")
            dictt=loads(accept_data)
            print(dictt)

    def temperaturereport(self):
        content={'type':1,'temperature':'%.2f' %self.realtimetemperature,'roomid':self.roomid}
        json_str = dumps(content)
        self.sendtcp(json_str)

    def requestreport(self):
        por={'type':0,'room':self.roomid,'switch':1,'temperature':self.realtimetemperature,'wind':self.windVelocity}
        json_str = dumps(por)
        self.sendtcp(json_str)

    def environmentchange(self):
        if self.targettemperature == self.realtimetemperature:
            return
        elif self.targettemperature > self.realtimetemperature:
            self.realtimetemperature += round(0.1 * self.windVelocity,2)
        else:
            self.realtimetemperature -= round(0.1 * self.windVelocity,2)

    def termtask(self):
        while True:
            sleep(6)
            self.environmentchange()
            self.temperaturereport()

    def edittask(self):
        self.requestreport()
        while True:
            self.interface()
            choice= input("please choice model:1:change temperature,2:change wind\n")
            if 1 == int(choice):
                num= input("please imput target\n")
                self.changetarget(int(num))
            elif 2 == int(choice):
                model= input("please input model\n")
                self.changemodle(int(model))
            else:
                print("valid input")


if __name__ == '__main__':
    Client1 = client("2015211301")
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = client_ui.Ui_MainWindow()
    ui.setupUi(MainWindow,Client1)
    MainWindow.show()
    sys.exit(app.exec_())












