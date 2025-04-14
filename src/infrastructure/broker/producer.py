import json
from dataclasses import dataclass
from aiokafka import AIOKafkaProducer

from core.entities import EmailMessage

from settings import get_settings

settings = get_settings()

@dataclass
class BrokerProducer:

    producer: AIOKafkaProducer
    topic: str

    async def open_connection(self) -> None:
        await self.producer.start()

    async def close_connection(self) -> None:
        await self.producer.stop()


    async def send_email(self, email_message: EmailMessage) -> None:
        
        encode_email_data = json.dumps(email_message.__dict__).encode()
        await self.producer.send(topic=self.email_topic, value=encode_email_data)




broker_producer = BrokerProducer(
    producer=AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers),
    topic="email_notifications"
)