from email.message import EmailMessage as EmailMessageOrig
import aiosmtplib
from core.entities.mail import EmailMessage
from logger import get_logger
from settings import get_settings

logger = get_logger()
settings = get_settings()


class AsyncSMTPMailer:

    def __init__(self):

        self.smtp = aiosmtplib.SMTP(
            hostname=settings.smtp_server,
            port=int(settings.smtp_port),
            use_tls=True
        )
        self.connected = False


    async def connect(self):
        
        if not self.connected:

            await self.smtp.connect()
            await self.smtp.login(settings.smtp_username, settings.smtp_password)
            self.connected = True


    async def send_email(self, email_message: EmailMessage):

        await self.connect()
        
        msg = EmailMessageOrig()
        msg['Subject'] = email_message.subject
        msg['From'] = settings.mail_from
        msg['To'] = email_message.email
        msg.set_content(email_message.body)

        try:
            await self.smtp.send_message(msg)
            logger.info(f"Email sent to {email_message.email}")
        
        except aiosmtplib.SMTPException as e:
            logger.error(f"Failed to send email to {email_message.email}: {e}")

        finally:
            await self.close()


    async def close(self):
        
        if self.connected:

            await self.smtp.quit()
            self.connected = False


SMTPClient: AsyncSMTPMailer = AsyncSMTPMailer()
