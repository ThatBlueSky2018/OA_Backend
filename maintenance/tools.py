from . import models
import datetime


class neworderid:
    numlength = 4

    @staticmethod
    def getnum(string):
        return int(string[len(string) - 4:len(string)])

    @staticmethod
    def initids():
        models.Order_Ids.objects.all().delete()
        models.Order_Ids.objects.create(date=datetime.date.today(), RP=0, RR=0, OFF=0, RA=0)

    @staticmethod
    def inttostr(num):
        strnum = str(num)
        while len(strnum) < neworderid.numlength:
            strnum = "0" + strnum
        return strnum

    @staticmethod
    def getnextRR():
        date = datetime.date.today()
        olddate = models.Order_Ids.objects.all().values("date")[0]["date"]
        if date != olddate:
            models.Order_Ids.objects.all().update(date=date, RR=0)
        RR = models.Order_Ids.objects.all().values("RR")[0]["RR"] + 1
        RR = neworderid.inttostr(RR)
        return "RR" + datetime.date.today().strftime("%Y%m%d") + RR

    @staticmethod
    def getnextRP():
        date = datetime.date.today()
        olddate = models.Order_Ids.objects.all().values("date")[0]["date"]
        if date != olddate:
            models.Order_Ids.objects.all().update(date=date, RP=0)
        RP = models.Order_Ids.objects.all().values("RP")[0]["RP"] + 1
        RP = neworderid.inttostr(RP)
        return "RP" + datetime.date.today().strftime("%Y%m%d") + RP

    @staticmethod
    def getnextOFF():
        date = datetime.date.today()
        olddate = models.Order_Ids.objects.all().values("date")[0]["date"]
        if date != olddate:
            models.Order_Ids.objects.all().update(date=date, OFF=0)
        OFF = models.Order_Ids.objects.all().values("OFF")[0]["OFF"] + 1
        OFF = neworderid.inttostr(OFF)
        return "OFF" + datetime.date.today().strftime("%Y%m%d") + OFF

    @staticmethod
    def getnextRA():
        date = datetime.date.today()
        olddate = models.Order_Ids.objects.all().values("date")[0]["date"]
        if date != olddate:
            models.Order_Ids.objects.all().update(date=date, RA=0)
        RA = models.Order_Ids.objects.all().values("RA")[0]["RA"] + 1
        RA = neworderid.inttostr(RA)
        return "RA" + datetime.date.today().strftime("%Y%m%d") + RA


class fortime:
    @staticmethod
    def nowdatetime():
        now = datetime.datetime.now()
        return now.replace(microsecond=0)

    @staticmethod
    def time_to_str(dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def str_to_time(str):
        return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def defaulttime():
        return datetime.datetime(2999, 1, 1, 1, 1, 1)