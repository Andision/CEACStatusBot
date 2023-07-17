from abc import ABC, abstractmethod

class CaptchaHandle(ABC):
    def __init__(self) -> None:
        super().__init__() 

    @abstractmethod
    def solve(self,image) -> str:
        pass