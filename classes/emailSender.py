from flask_mail import Mail, Message
import os
from abc import ABC, abstractmethod
from typing import List, Optional
from flask import current_app as app

class SendenEmail(ABC):
    @abstractmethod
    def Send(self, subject: str, body: str, recipients: List[str], sender: Optional[str] = None) -> None:
        ...


class GmailSmtpEmailSender(SendenEmail):
    def __init__(self, mail: Mail):
        self.mail = mail

    def Send(self, subject: str, body: str, recipients: List[str], sender: Optional[str] = None) -> None:

        _sender = sender or app.config.get('MAIL_USERNAME') or app.config.get('MAIL_DEFAULT_SENDER')
        message = Message(subject=subject, sender=_sender, recipients=recipients, body=body)
        self.mail.send(message)