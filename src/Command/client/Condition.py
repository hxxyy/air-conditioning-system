from threading import Thread
from client.mainwindow import Client

class UseThread(Thread):
    def __init__(self, counter):
        Thread.__init__(self)
        self.counter = counter

    def run(self):
        if self.counter == 1:
            testClient.termtask()
        else:
            testClient.edittask()

if __name__=='__main__':
    ip=input("ip address")
    testClient = Client(adress=ip)
    thread1 = UseThread(1)
    thread2 = UseThread(2)
    # 开启新线程
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()