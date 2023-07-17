import os
from CEACStatusBot import query_status,OnnxCaptchaHandle

try:
    LOCATION = os.environ["LOCATION"]
    NUMBER = os.environ["NUMBER"]
    print(query_status(LOCATION,NUMBER,OnnxCaptchaHandle("captcha.onnx")))
except KeyError:
    print("ENV Error")
