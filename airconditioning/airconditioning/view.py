from django.http import HttpResponse
from django.shortcuts import render,HttpResponseRedirect
from airconditioning.mainwindow import *
from manage import Client1


def login(request):
    context={}
    return render(request,'login.html',context)

'''
def loginsubmit(request):
    context = {}
    request.encoding = 'utf-8'
    context['roomid']=request.GET['id']
    for q in Clientlist:
        if request.GET['id']==q.roomid:
            Client1.roomid=request.GET['id']
            Client1.adress= request.GET['ip']
            context['address'] = request.GET['ip']
            return render(request,'client.html',context)

    Client1.roomid = request.GET['id']
    Client1.adress = request.GET['ip']
    Clientlist.append(Client1)
    print("here!")
    return render(request, 'client.html', context)
'''

def loginsubmit(request):
    context = {}
    request.encoding = 'utf-8'
    context['roomid']=request.GET['id']
    Client1.roomid=request.GET['id']
    Client1.adress= request.GET['ip']
    context['address'] = request.GET['ip']
    return render(request,'client.html',context)


def ini():
    context = {}
    context['roomid'] = Client1.roomid
    context['target'] = Client1.targettemperature
    context['realtem'] = format(Client1.realtimetemperature, '.2f')
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
    Client1.changeswitch()
    context = ini()
    return HttpResponseRedirect("/client")

#风速
def wind0(request):
    Client1.changemodle(0)
    return HttpResponseRedirect("/client")

def wind1(request):
    Client1.changemodle(1)
    return HttpResponseRedirect("/client")

def wind2(request):
    Client1.changemodle(2)
    return HttpResponseRedirect("/client")

def up(request):
    Client1.targettemperature +=1
    return HttpResponseRedirect("/client")

def down(request):
    Client1.targettemperature -=1
    return HttpResponseRedirect("/client")
