from server.Airserver import MainServer
from threading import Thread
class UseThread(Thread):
    def __init__(self, counter):
        Thread.__init__(self)
        self.counter = counter

    def run(self):
        if self.counter == 1:
            testServer.ConnectClient()
        else:
            testServer.editTask()

if __name__=='__main__':
    dPort=input("请输入服务端口:")
    maxsize = input("请输入最大服务数:")
    testServer = MainServer(int(maxsize),int(dPort))
    thread1 = UseThread(1)
    thread2 = UseThread(2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()