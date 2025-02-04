import os
from CEACStatusBot import query_status,OnnxCaptchaHandle

try:
    NUMBER = os.environ["NUMBER"]
    print(query_status(NUMBER,OnnxCaptchaHandle("captcha.onnx")))
except KeyError:
    print("ENV Error")
