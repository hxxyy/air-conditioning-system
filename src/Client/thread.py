#!/usr/bin/python3
import threading
import mainwindow

t1=mainwindow.client("2015211301")
class myThread (threading.Thread):
    def __init__(self, counter):
        threading.Thread.__init__(self)
        self.counter = counter
    def run(self):
        if self.counter==1:
           t1.termtask()
        else:
           t1.edittask()


# 创建新线程
thread1 = myThread(1)
thread2 = myThread(2)

# 开启新线程
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print ("退出主线程")
