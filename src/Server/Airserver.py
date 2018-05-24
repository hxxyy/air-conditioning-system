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
    __serverSize = 5
    __feeSpeed = 1

    def ConnectClient(self, host=__ipAdress, port=__BindPort, maxlisten=8):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen(maxlisten)
            while True:
                conn, addr = s.accept()
                print('accept:', addr)
                while True:
                    accept_data = str(conn.recv(1024), encoding="utf8")
                    massage = json.loads(accept_data)
                    error = 0
                    print("".join(["接收报文:", accept_data, "客户端口：", str(addr[1])]))  # 可以删去
                    if massage['room'] not in self.__clientList and len(self.__clientList)<self.__clientNum and len(massage) == 5:
                        clientItem = {}
                        clientItem['room'] = massage['room']
                        clientItem['targettemp'] = massage['temperature']
                        clientItem['realtimetemp'] = 30.00
                        clientItem['WindVelocity'] = 0
                        clientItem['switch'] = massage['switch']
                        clientItem['cost'] = 0.00
                        self.__clientList[clientItem['roomid']] = clientItem

                    if len(massage) == 3:
                        if 'room' not in massage or 'temperature' not in massage or massage['room'] not in self.__clientList:
                            error = 1
                        else:
                            self.__clientList[massage['room']]['realtimetemp']=massage['temperature']
                    elif len(massage) == 5:
                        if 'room' not in massage or 'temperature' not in massage or massage['room'] not in self.__clientList:
                            error = 1
                        else:
                            self.__clientList[massage['room']]['targettemp']=massage['temperature']
                            self.__clientList[massage['room']]['WindVelocity'] = massage['wind']
                            self.__clientList[massage['room']]['switch'] = massage['switch']
                    else:
                        error =1
                    if error ==1:
                        send_data = {'switch': 0,
                                     'temperature': 30.00,
                                     'wind':0,
                                     'cost': 0.00}
                        sendd = json.dumps(send_data)
                        conn.sendall(bytes(sendd, encoding="utf8"))
                        break
                    else:
                        self.Dispatch()

                        send_data = {'switch': self.__clientList[massage['room']]['switch'],
                                     'temperature': self.__clientList[massage['room']]['realtimetemp'],
                                     'wind': self.__clientList[massage['room']]['WindVelocity'],
                                     'cost': self.__clientList[massage['room']]['cost']}
                        self.__clientList[massage['room']]['cost']+= self.__clientList[massage['room']]['WindVelocity']*self.__feeSpeed
                        sendd = json.dumps(send_data)
                        conn.sendall(bytes(sendd, encoding="utf8"))
                        break

    def setFeerate(self, newFee):
        self.__feeSpeed = newFee

    def printinfo(self,room):
        pass
    def mysqlmanage(self,massage,choice):
        db = pymysql.connect(
            host="localhost",
            port=3306,
            user="wx",
            passwd="password",
            db="mytest")
        cursor = db.cursor()
        sql=massage
        if choice ==1:
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # 如果发生错误则回滚
                db.rollback()
        else:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        # 关闭数据库连接
        db.close()

    def Dispatch(self):
        for key in self.__clientList:
            if self.__clientList[key]['room'] not in self.__servelist:
                if self.__clientList[key]['switch'] == 1:
                    dif = self.__clientList[key]['targettemp'] - self.__clientList[key]['realtimetemp']
                    if dif < 0.0:
                        dif = 0.0 - dif
                    if dif > 0.5:
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
                    self.__servelist.remove(self.__clientList[key]['roomid'])

    def DailyRecord(self, choice):
        pass


if __name__ == '__main__':
    pass
