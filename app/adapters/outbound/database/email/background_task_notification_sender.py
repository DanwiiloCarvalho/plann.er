import uuid
from app.adapters.outbound.database.email.smtp_email_sender import SMTPEmailSender
from app.domain.ports.output_ports.notification_sender import NotificationSender
from fastapi import BackgroundTasks


class BackgroundTaskNotificationSender(NotificationSender):
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        smtp_email_sender: SMTPEmailSender
    ) -> None:
        self.__background_tasks = background_tasks
        self.__smtp_email_sender = smtp_email_sender

    def send_notification(self, emails_list: list[str], message: str) -> None:
        self.__background_tasks.add_task(
            self.__smtp_email_sender.send_trip_confirmation,
            emails_list,
            message
        )
