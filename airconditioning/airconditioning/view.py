from django.http import HttpResponse
from django.shortcuts import render,HttpResponseRedirect
from airconditioning.mainwindow import *
from threading import Thread
from airconditioning.mainwindow import Client

global Client1

class UseThread(Thread):
    global Client1
    def __init__(self, counter):
        Thread.__init__(self)
        self.counter = counter

    def run(self):
        if self.counter == 1:
            Client1.termtask()
        else :
            Client1.edittask()


def login(request):
    context={}
    return render(request,'login.html',context)


def loginsubmit(request):
    request.encoding = 'utf-8'
    global Client1
    Client1=Client(rid=request.GET['id'],adress=request.GET['ip'],tport=int(request.GET['port']))
    Client1.requestreport()
    thread1 = UseThread(1)
    thread1.start()
    #thread1.join()
    return render(request,'client.html')


def ini():
    global Client1
    context = {}
    context['roomid'] = Client1.roomid
    context['target'] = Client1.targettemperature
    context['realtem'] = float(format(Client1.realtimetemperature, '.2f'))
    context['wind'] = Client1.windVelocity
    context['mode'] = Client1.switch
    context['uplimit'] = Client1.uplimit
    context['downlimit'] = Client1.lowlimit
    context['fee'] = Client1.money
    return  context


def initial(request):
    context = ini()
    return render(request,'client.html',context)

# 开关
def onoff(request):
    global Client1
    Client1.changeswitch()
    context = ini()
    return HttpResponseRedirect("/client")

#风速
def wind0(request):
    global Client1
    Client1.changemodle(0)
    return HttpResponseRedirect("/client")

def wind1(request):
    global Client1
    Client1.changemodle(1)
    return HttpResponseRedirect("/client")

def wind2(request):
    global Client1
    Client1.changemodle(2)
    return HttpResponseRedirect("/client")

#调温
def up(request):
    global Client1
    Client1.targettemperature +=1
    if Client1.targettemperature>Client1.uplimit:
        Client1.targettemperature -= 1
    Client1.changetarget(Client1.targettemperature)
    return HttpResponseRedirect("/client")

def down(request):
    global Client1
    Client1.targettemperature -=1
    if Client1.targettemperature<Client1.lowlimit:
        Client1.targettemperature += 1
    Client1.changetarget(Client1.targettemperature)
    return HttpResponseRedirect("/client")
