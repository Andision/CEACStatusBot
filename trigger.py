import os
from CEACStatusBot import NotificationManager,EmailNotificationHandle,TelegramNotificationHandle


try:
    LOCATION = os.environ["LOCATION"]
    NUMBER = os.environ["NUMBER"]
    PASSPORT_NUMBER = os.environ["PASSPORT_NUMBER"]
    SURNAME = os.environ["SURNAME"]
    notificationManager = NotificationManager(LOCATION,NUMBER,PASSPORT_NUMBER,SURNAME)
except KeyError:
    print("LOCATION or NUMBER Error")

try:
    FROM = os.environ["FROM"]
    TO = os.environ["TO"]
    PASSWORD = os.environ["PASSWORD"]
    SMTP = os.environ.get("SMTP", "")
    if FROM and TO and PASSWORD:
        emailNotificationHandle = EmailNotificationHandle(FROM,TO,PASSWORD,SMTP)
        notificationManager.addHandle(emailNotificationHandle)
except KeyError:
    print("Email notification config error")

try:
    BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
    CHAT_ID = os.environ["TG_CHAT_ID"]
    if BOT_TOKEN and CHAT_ID:
        tgNotif = TelegramNotificationHandle(BOT_TOKEN,CHAT_ID)
        notificationManager.addHandle(tgNotif)
except KeyError:
    print("Telegram bot notification config error")

notificationManager.send()
