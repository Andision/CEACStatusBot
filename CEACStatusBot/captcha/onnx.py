from PIL import Image
from io import BytesIO
import onnxruntime as ort
import numpy as np
import string

from .handle import CaptchaHandle

class OnnxCaptchaHandle(CaptchaHandle):
    def __init__(self,onnxModelPath:str='captcha.onnx') -> None:
        super().__init__()
        self.__onnxModelPath = onnxModelPath

    def __decode(self,sequence):
        characters = '-' + string.digits + string.ascii_uppercase
        a = ''.join([characters[x] for x in sequence])
        s = ''.join([x for j, x in enumerate(a[:-1]) if x != characters[0] and x != a[j+1]])
        if len(s) == 0:
            return ''
        if a[-1] != characters[0] and s[-1] != a[-1]:
            s += a[-1]
        return s

    def solve(self,image) -> str:
        img = np.asarray( Image.open(BytesIO(image)) ,dtype=np.float32) / 255.0
        img = np.expand_dims(np.transpose(img,(2,0,1)), axis=0)
        ort_sess = ort.InferenceSession(self.__onnxModelPath)
        outputs = ort_sess.run(None, {'input': img})
        x = outputs[0]
        t = np.argmax( np.transpose(x,(1,0,2)), -1)
        pred = self.__decode(t[0])
        return pred