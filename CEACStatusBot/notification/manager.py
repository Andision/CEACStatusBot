from .handle import NotificationHandle
from CEACStatusBot.request import query_status
from CEACStatusBot.captcha import CaptchaHandle,OnnxCaptchaHandle

class NotificationManager():
    def __init__(self,location:str,number:str,captchaHandle:CaptchaHandle=OnnxCaptchaHandle("captcha.onnx")) -> None:
        self.__handleList = []
        self.__location = location
        self.__number = number
        self.__captchaHandle = captchaHandle

    def addHandle(self, notificationHandle:NotificationHandle) -> None:
        self.__handleList.append(notificationHandle)

    def send(self,) -> None:
        res = query_status(self.__location,self.__number, self.__captchaHandle)

        if res['status'] == "Refused":
            import os,pytz,datetime
            try:
                TIMEZONE = os.environ["TIMEZONE"]
                localTimeZone = pytz.timezone(TIMEZONE)
                localTime = datetime.datetime.now(localTimeZone)
            except pytz.exceptions.UnknownTimeZoneError:
                print("UNKNOWN TIMEZONE Error, use default")
                localTime = datetime.datetime.now()
            except KeyError:
                print("TIMEZONE Error")
                localTime = datetime.datetime.now()

            if localTime.hour <8 or localTime.hour>22:
                print("In Manager, no disturbing time")
                return
            if localTime.minute >30:
                print("In Manager, no disturbing time")
                return

        for notificationHandle in self.__handleList:
            notificationHandle.send(res)
