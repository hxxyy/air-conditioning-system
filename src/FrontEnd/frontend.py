import socket
import time
import json
class front:

    def __init__(self,clnumber=0,maxnumber=8,adress='127.0.0.1',tport=8086):
        print("欢迎来到快捷酒店，这里很穷")
        self.clientnumber=clnumber
        self.maxnumber=maxnumber
        self.adress = adress
        self.port = tport
        self.roomtable={'1':{'id':'','fee':0},'2':{'id':'','fee':0},'3':{'id':'','fee':0},'4':{'id':'','fee':0},'5':{'id':'','fee':0},'6':{'id':'','fee':0},'7':{'id':'','fee':0},'8':{'id':'','fee':0}}

    def welcome(self):
        id = input("请输入身份证号：")#客户ID，随便几位
        if self.clientnumber<self.maxnumber:
            for key in self.roomtable:
                if self.roomtable[key]['id'] == '':
                    self.roomtable[key]['id'] = id
                    self.clientnumber += 1
                    data={'roomid':key,'id':id}
                    self.sendtcp(json.dumps(data),1)
                    break
        else:
            print("满客")

    def goodbye(self,roomid):
        send_data = {'quitid': roomid}
        self.sendtcp(json.dumps(send_data),1)

        tempdata=self.sendtcp('we',2)
        print('很高兴为您服务，你的id是{id},你的欠费是{fee}'.format(id=tempdata['id'],fee=tempdata['fee']))
        print('收费')
        self.roomtable[roomid]={'id':'','fee':0}

    def sendtcp(self,senddata,choice):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.adress, self.port))
            s.sendall(bytes(senddata, encoding="utf8"))
            if 1 != choice:
                while True:
                    accept_data = s.recv(1024)
                    a=str(accept_data,encoding="utf8")
                    if len(a)>10:
                        return eval(accept_data)
            s.close()

    def run(self):
        while True:
            for key in self.roomtable:
                print(self.roomtable[key])
            print("住店：1，退房：2")
            id = input("请输入选择：")
            if id =='1':
                self.welcome()
            elif id == '2':
                cid = input("请输入选择：")
                self.goodbye(cid)
            else:
                print("valid choice:")

if __name__=='__main__':
    f1=front()
    f1.run()



