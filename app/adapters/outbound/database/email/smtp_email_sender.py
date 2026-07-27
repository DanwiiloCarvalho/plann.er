from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from app.infrastructure.config import settings


class SMTPEmailSender:
    def send_trip_confirmation(
        self,
        to_addresses: list[str],
        message: str
    ) -> None:
        from_address = settings.EMAIL_USERNAME  # variável de ambiente
        password = settings.EMAIL_PASSWORD  # variável de ambiente

        email_msg = MIMEMultipart('alternative')
        email_msg['from'] = 'trip_confirmation@planner.com'
        email_msg['to'] = ', '.join(to_addresses)
        email_msg['subject'] = 'Confirmação de viagem'
        email_msg.attach(MIMEText(message, 'plain', 'utf-8'))

        with SMTP(host='smtp.ethereal.email', port=587) as server:
            server.starttls()
            server.login(from_address, password)

            for address in to_addresses:
                server.sendmail(from_address, address, email_msg.as_string())
