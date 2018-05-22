import socket
import json
import pymysql
import AirTime


class MainServer:
    __clientList = {}
    __servelist = []  # 对这个队列中的每一个用户计费，根据他们的风速计费
    __clientNum = 8
    __ipAdress = '127.0.0.1'
    __BindPort = 8808
    __serverSize=5

    def init(self):
        i = 0
        clientItem = {}
        while i < self.__clientNum:
            clientItem['roomid'] = str(self.__clientNum + 1)
            clientItem['targettemp'] = 26
            clientItem['realtimetemp'] = 30
            clientItem['windVelocity'] = 0
            clientItem['switch'] = 0
            clientItem['cost'] = 0.0
            self.__clientList[clientItem['roomid']]=clientItem
            clientItem = {}
            i = i + 1

    def termtask(self):
        self.Dispatch()#调度

    def normaltask(self):
        pass

    def Dispatch(self):
        for key,value in self.__clientList:
            if value['roomid'] not in self.__servelist:
                if value['switch'] == 1:
                    dif=value['targettemp']-value['realtimetemp']
                    if dif<0:
                        dif = 0-dif
                    if dif>1:
                        if len(self.__servelist)<self.__serverSize:
                            self.__servelist.append(value['roomid'])
                        elif value['windVelocity'] == 0:
                            continue
                        elif value['windVelocity'] == 1:
                            for serveritem in self.__servelist:
                                if self.__clientList[serveritem]['windVelocity'] == 0:
                                    self.__servelist.remove(serveritem)
                                    self.__servelist.append(value['roomid'])
                                    break
                            if value['roomid'] not in self.__servelist:
                                print("没有合适的空调资源")
                        elif value['windVelocity'] == 2:
                            for serveritem in self.__servelist:
                                if self.__clientList[serveritem]['windVelocity'] < 2:
                                    self.__servelist.remove(serveritem)
                                    self.__servelist.append(value['roomid'])
                                    break
                            if value['roomid'] not in self.__servelist:
                                self.__servelist.remove(self.__servelist[0])
                                self.__servelist.append(value['roomid'])
                    else:
                        continue
                else:
                    continue
            else:
                dif = value['targettemp'] - value['realtimetemp']
                if dif < 0:
                    dif = 0 - dif
                if dif < 1 :
                    self.__servelist.remove(value['roomid'])
                continue


    def DailyRecord(self, choice):
        pass


if __name__ == '__main__':
    pass
