from abc import ABC, abstractmethod
import uuid


class NotificationSender(ABC):
    @abstractmethod
    def send_notification(self, emails_list: list[str], message: str) -> None:
        pass
