from socket import socket, AF_INET, SOCK_STREAM
from json import loads

class FrontEnd:
    def __init__(self, maxnumber=2, tport=8086, adr='10.128.248.231'):
        self.__maxnumber = maxnumber
        self.__port = tport
        self.__adress = adr

    def recieve(self):
        with socket(AF_INET, SOCK_STREAM) as s:
            s.bind((self.__adress, self.__port))
            s.listen(self.__maxnumber)
            while True:
                conn, addr = s.accept()
                accept_data = str(conn.recv(1024), encoding="utf8")
                ans = loads(accept_data)
                print('your room:', ans['room'])
                print('your item:', ans['item'])
                print('your fee:', ans['fee'])

if __name__ == '__main__':
    f1 = FrontEnd()
    f1.recieve()
