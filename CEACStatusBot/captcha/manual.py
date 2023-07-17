
from .handle import CaptchaHandle

class ManualCaptchaHandle(CaptchaHandle):
    def __init__(self) -> None:
        super().__init__()

    def solve(self,image) -> str:
        # imgdata = base64.b64decode(image)
        file = open('captcha.jpg','wb')
        file.write(image)
        file.close()
        res = input("Input Catpcha: ")
        return res