from abc import ABC, abstractmethod

class NotificationHandle(ABC):
    def __init__(self) -> None:
        super().__init__() 

    @abstractmethod
    def send(self,result):
        pass