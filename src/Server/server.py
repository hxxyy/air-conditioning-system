import socket
import json
def conne(host="192.168.43.110",port=9008,maxlisten = 5):
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


if __name__=="__main__":
    conne()
