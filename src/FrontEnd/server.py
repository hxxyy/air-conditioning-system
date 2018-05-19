import socket
import json
import time

"""

def conne(host="127.0.0.1",port=8086,maxlisten = 5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(maxlisten)
        while True:
            conn, addr = s.accept()
            send_data = {'switch': 1, 'temperature': 25, 'wind': 1, 'cost': 2.00}
            sendd = json.dumps(send_data)
            conn.sendall(bytes(sendd, encoding="utf8"))
            while True:
                accept_data = str(conn.recv(1024),encoding="utf8")
                print("".join(["接收报文", accept_data, "客户端口：", str(addr[1])]))
                #if accept_data == "byebye":  # 如果接收到“byebye”则跳出循环结束和第一个客户端的通讯，开始与下一个客户端进行通讯
                 #   break

                break

"""
def conne(host="127.0.0.1",port=8086,maxlisten = 5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(maxlisten)
        while True:
            conn, addr = s.accept()

            accept_data = str(conn.recv(1024), encoding="utf8")

            if len(accept_data)>16:
                print("".join(["接收报文", accept_data, "客户端口：", str(addr[1])]))
            else:
                send_data = {'id': '2015', 'fee': 2.00}
                sendd = json.dumps(send_data)
                conn.sendall(bytes(sendd, encoding="utf8"))
            conn.close()

if __name__=="__main__":
    conne()