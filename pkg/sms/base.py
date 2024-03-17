from abc import ABC, abstractmethod


class Sms(ABC):

    @abstractmethod
    def send(self, message: str) -> None:
        pass
