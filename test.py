import os
from CEACStatusBot import query_status,OnnxCaptchaHandle

try:
    LOCATION = os.environ["LOCATION"]
    NUMBER = os.environ["NUMBER"]
    PASSPORT_NUMBER = os.environ["PASSPORT_NUMBER"]
    SURNAME = os.environ["SURNAME"]
    print(query_status(LOCATION,NUMBER,PASSPORT_NUMBER,SURNAME,OnnxCaptchaHandle("captcha.onnx")))
except KeyError:
    print("ENV Error")
