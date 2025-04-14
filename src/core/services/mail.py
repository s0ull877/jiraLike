from dataclasses import dataclass
from uuid import UUID

from core.entities import EmailMessage
from core.Ibroker import IBrokerProducer

from settings import get_settings


settings = get_settings()

@dataclass
class MailService:
    
    def __init__(
        self,
        broker_producer: IBrokerProducer,
    ):
        
        self.broker_producer = broker_producer


    async def send_verify_code(self, to: str, code: UUID) -> None:
        
        # создаем код верификации привязанный к почте

        email_message = EmailMessage(
            email=to, 
            subject=f"Verification code for {to}", 
            body=f"Go to {settings.server_url}/verify/{code} for verifyiong your account"
        )


        await self.broker_producer.send_email(email_message=email_message)

        return



