import os
from CEACStatusBot import NotificationManager,EmailNotificationHandle


try:
    LOCATION = os.environ["LOCATION"]
    NUMBER = os.environ["NUMBER"]
    notificationManager = NotificationManager(LOCATION,NUMBER)
except KeyError:
    print("LOCATION or NUMBER Error")

try:
    FROM = os.environ["FROM"]
    TO = os.environ["TO"]
    PASSWORD = os.environ["PASSWORD"]
    emailNotificationHandle = EmailNotificationHandle(FROM,TO,PASSWORD)
    notificationManager.addHandle(emailNotificationHandle)
except KeyError:
    print("EMAIL Error")

notificationManager.send()
