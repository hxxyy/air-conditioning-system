from time import strftime,localtime

class MainTime:
    def NowTime(self):
        return strftime("%m%d%H%M%S", localtime())

    def TimeDiff(self, Timestring1, Timestring2):#Timestring1
        m = int(Timestring1[0:2]) - int(Timestring2[0:2])
        d = int(Timestring1[2:4]) - int(Timestring2[2:4])
        h = int(Timestring1[4:6]) - int(Timestring2[4:6])
        n = int(Timestring1[6:8]) - int(Timestring2[6:8])
        s = int(Timestring1[8:10]) - int(Timestring2[8:10])
        ans = m * 86400 * 30 + d * 86400 + h * 3600 + n * 60 + s
        return ans

    def NowMonth(self):
        return strftime("%m", localtime())

    def NowDay(self):
        return strftime("%d", localtime())

    def NowHour(self):
        return strftime("%H", localtime())

    def NowMinute(self):
        return strftime("%M", localtime())

    def NowSecond(self):
        return strftime("%S", localtime())

if __name__=='__main__':#非主程序不会运行
    t=MainTime()
    print(t.NowTime())
    print(t.NowHour())
    print(t.TimeDiff('0328142813','0328151214'))