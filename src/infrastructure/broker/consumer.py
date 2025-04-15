import json
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
        
        await self.open_connection()
        
        try:
        
            async for message in self.consumer:
                
                try:
                
                    data = json.loads(message.value.decode())
                    email_message = EmailMessage(**data)
                    SMTPClient.send_email(email_message)
                
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
        
        finally:
        
            await self.close_connection()





broker_consumer = BrokerConsumer(
    consumer=AIOKafkaConsumer(
        'email_notifications',
        bootstrap_servers=settings.kafka_bootstrap_servers,
        value_deserializer=lambda message: json.loads(message.decode("utf-8")),
    )
)