import socket
import json
import pymysql
import AirTime

class MainServer:
    __clientList = []
    __servelist = []#对这个队列中的每一个用户计费，根据他们的风速计费
    __clientNum = 8
    __ipAdress='127.0.0.1'
    __BindPort= 8808
    def init(self):
        i = 0
        clientItem={}
        while i<self.__clientNum:
            clientItem['roomid']=str(self.__clientNum+1)
            clientItem['targettemp']=26
            clientItem['realtimetemp']= 30
            clientItem['windVelocity'] = 0
            self.__clientList.append(clientItem)
            clientItem={}
            i=i+1


    def termtask(self):
        pass

    def normaltask(self):
        pass

    def Dispatch(self):
        pass

    def DailyRecord(self):
        pass

if __name__=='__main__':
    pass
