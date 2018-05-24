from socket import AF_INET, SOCK_STREAM, gethostbyname, gethostname, socket, SOL_SOCKET, SO_KEEPALIVE
from json import loads, dumps
from pymysql import connect
from AirTime import NowTime, TimeDiff, dayegotime


class MainServer:
    def __init__(self, serversize=8, bPort=8080):
        self.__clientList = {}
        self.__servelist = []  # 对这个队列中的每一个用户计费，根据他们的风速计费
        self.__clientNum = serversize
        self.__ipAdress = gethostbyname(gethostname())
        self.__BindPort = bPort
        self.__serverSize = 5
        self.__feeSpeed = 1

    def ConnectClient(self):
        with socket(AF_INET, SOCK_STREAM) as s:
            s.bind((self.__ipAdress, self.__BindPort))
            print('local ip:', self.__ipAdress)
            s.listen(self.__clientNum)
            while True:
                conn, addr = s.accept()
                while True:
                    accept_data = str(conn.recv(1024), encoding="utf8")
                    massage = loads(accept_data)
                    error = 0
                    print("".join(["报文:", accept_data, "Port:", str(addr[1]), "-Ip:", str(addr[0])]))  # 可以删去
                    if massage['room'] not in self.__clientList and len(self.__clientList) < self.__clientNum and len(
                            massage) == 5:
                        clientItem = {}
                        clientItem['room'] = massage['room']
                        clientItem['targettemp'] = float(massage['temperature'])
                        clientItem['realtimetemp'] = 30.00
                        clientItem['WindVelocity'] = 0
                        clientItem['switch'] = int(massage['switch'])
                        clientItem['cost'] = 0.00
                        self.__clientList[clientItem['room']] = clientItem
                        print('new client:', massage['room'])

                    if 'room' not in massage or 'temperature' not in massage or massage[
                        'room'] not in self.__clientList:
                        error = 1
                    elif len(massage) == 3:
                        self.__clientList[massage['room']]['realtimetemp'] = float(massage['temperature'])
                    elif len(massage) == 5:
                        self.__clientList[massage['room']]['targettemp'] = float(massage['temperature'])
                        self.__clientList[massage['room']]['WindVelocity'] = int(massage['wind'])
                        self.__clientList[massage['room']]['switch'] = int(massage['switch'])
                    else:
                        error = 1

                    if 1 == error:
                        print('error:', addr)
                        conn.sendall(
                            bytes(dumps({'switch': 0, 'temperature': 30.00, 'wind': 0, 'cost': 0.00}), encoding="utf8"))
                        break
                    else:
                        self.__Dispatch()

                        send_data = {'switch': int(self.__clientList[massage['room']]['switch']),
                                     'temperature': float(self.__clientList[massage['room']]['realtimetemp']),
                                     'wind': int(self.__clientList[massage['room']]['WindVelocity']),
                                     'cost': float(self.__clientList[massage['room']]['cost'])}
                        self.__clientList[massage['room']]['cost'] += self.__clientList[massage['room']][
                                                                          'WindVelocity'] * self.__feeSpeed
                        sendd = dumps(send_data)
                        conn.sendall(bytes(sendd, encoding="utf8"))
                        self.__mysqlmanage(
                            'insert into AirLog values (' + str(NowTime()) + ',"' + massage['room'] + '",' + str(
                                send_data['wind']) + ');', 1)
                        break

    def __setserverSize(self, newsize):
        if newsize > 3 and newsize < self.__clientNum:
            self.__serverSize = newsize

    def __setFeerate(self, newFee):
        self.__feeSpeed = newFee

    def __printinfo(self, term=2):  # termExample:20
        massage = 'select * from AirLog where time >' + dayegotime(NowTime(), term) + ';'
        li = self.__mysqlmanage(massage, 2)
        for line in li:
            print(line)

    def __mysqlmanage(self, massage, choice):
        db = connect(
            host="localhost",
            port=3306,
            user="wx",
            passwd="password",
            db="mytest")
        cursor = db.cursor()
        sql = massage
        if choice == 1:
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # 如果发生错误则回滚
                db.rollback()
        elif choice == 2:
            cursor.execute(sql)
            result = cursor.fetchall()
            db.close()
            return result
        # 关闭数据库连接
        db.close()

    def __Dispatch(self):
        for key in self.__clientList:
            if self.__clientList[key]['room'] not in self.__servelist:
                if self.__clientList[key]['switch'] == 1:
                    dif = self.__clientList[key]['targettemp'] - self.__clientList[key]['realtimetemp']
                    if dif < 0.0:
                        dif = 0.0 - dif
                    if dif > 0.7:
                        if len(self.__servelist) < self.__serverSize:
                            self.__servelist.append(self.__clientList[key]['room'])
                        elif self.__clientList[key]['windVelocity'] == 1:
                            for serveritem in self.__servelist:
                                if self.__clientList[serveritem]['windVelocity'] == 0:
                                    self.__servelist.remove(serveritem)
                                    self.__servelist.append(self.__clientList[key]['room'])
                                    break
                        elif self.__clientList[key]['windVelocity'] == 2:
                            for serveritem in self.__servelist:
                                if self.__clientList[serveritem]['windVelocity'] < 2:
                                    self.__servelist.remove(serveritem)
                                    self.__servelist.append(self.__clientList[key]['room'])
                                    break
                            if self.__clientList[key]['room'] not in self.__servelist:
                                self.__servelist.remove(self.__servelist[0])
                                self.__servelist.append(self.__clientList[key]['room'])
            else:
                dif = self.__clientList[key]['targettemp'] - self.__clientList[key]['realtimetemp']
                if dif < 0.0:
                    dif = 0.0 - dif
                if dif < 0.2:
                    self.__clientList[key]['WindVelocity'] = 0
                    self.__servelist.remove(self.__clientList[key]['room'])

    def __statement(self, room):
        massage = 'select * from AirLog where room = "' + room + '";'
        li = self.__mysqlmanage(massage, 2)
        with socket(AF_INET, SOCK_STREAM) as sc:
            sc.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
            sc.connect(('127.0.0.1', 8086))
            send_data = {'room': room, 'item': li, 'fee': self.__clientList[room]['cost']}
            sc.sendall(bytes(dumps(send_data), encoding="utf8"))

    def editTask(self):
        while True:
            print('server size:', self.__serverSize)
            print('fee speed:', self.__feeSpeed)
            choice = int(input("1:set serversize,2:set feespeed,3:exit air,4:print info"))
            if choice == 1:
                size = int(input("server size:"))
                self.__setserverSize(size)
            elif choice == 2:
                size = int(input("server size:"))

                self.__setFeerate(size)
            elif choice == 3:
                size = input("room id")
                if size in self.__clientList:
                    self.__clientList.pop(size)
                    self.__servelist.remove(size)
                    self.__statement(size)
            elif choice == 4:
                self.__printinfo()
            else:
                print("error choice")


if __name__ == '__main__':
    test = MainServer()
    test.ConnectClient()
