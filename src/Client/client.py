#!/usr/bin/python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("127.0.0.1", 9008))
    while True:
        send_data = input("输入发送内容:")
        s.sendall(bytes(send_data, encoding="utf8"))
        if send_data == "byebye":
            break
        accept_data = str(s.recv(1024), encoding="utf8")
        print("".join(("接收内容：", accept_data)))
    s.close()
