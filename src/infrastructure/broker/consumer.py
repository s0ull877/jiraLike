import json
import asyncio
from dataclasses import dataclass
from aiokafka import AIOKafkaConsumer

from core.entities.mail import EmailMessage
from logger import get_logger
from settings import get_settings

from infrastructure.SMTPclient import SMTPClient

logger = get_logger()
settings = get_settings()

@dataclass
class BrokerConsumer:
    
    consumer: AIOKafkaConsumer


    async def open_connection(self) -> None:
        await self.consumer.start()


    async def close_connection(self) -> None:
        await self.consumer.stop()


    async def consume_callback_message(self) -> None:
        
        async for message in self.consumer:
            
            try:
            
                email_message = EmailMessage(**message.value)
                logger.info(f"sending email...")
                asyncio.create_task(SMTPClient.send_email(email_message))
                
            
            except Exception as e:
                logger.error(f"Error processing message: {e}")
        




broker_consumer = BrokerConsumer(
    consumer=AIOKafkaConsumer(
        'email_notifications',
        group_id="email_notification_group",
        bootstrap_servers=settings.kafka_bootstrap_servers,
        value_deserializer=lambda message: json.loads(message.decode("utf-8")),
    )
)