from dataclasses import dataclass
import aio_pika
from aio_pika.exceptions import QueueEmpty
from aiormq import AMQPConnectionError
from src.settings.settings import settings


@dataclass
class BrokerService:
    broker_url: settings.broker_settings.broker_full_url

    async def get_user_email_from_broker(self) -> dict:
        """Получить email из RabbitMQ"""
        try:
            connection = await aio_pika.connect_robust(url=self.broker_url)
        except AMQPConnectionError:
            raise Exception('Cannot connect to broker')

        queue_name = "email_register_queue"

        async with connection:
            channel = await connection.channel()

            await channel.set_qos(prefetch_count=5)

            queue = await channel.declare_queue(queue_name)
            try:
                incoming_message = await queue.get(timeout=5)
                await incoming_message.ack()
                return incoming_message.body
            except QueueEmpty:
                return None

    async def get_password_change_code_from_broker(self) -> dict:
        """Код смены пароля и временный пароль из RabbitMQ"""
        try:
            connection = await aio_pika.connect_robust(url=self.broker_url)
        except AMQPConnectionError:
            raise Exception('Cannot connect to broker')

        queue_name = "change_password_codes"

        async with connection:
            channel = await connection.channel()

            await channel.set_qos(prefetch_count=5)

            queue = await channel.declare_queue(queue_name)
            try:
                incoming_message = await queue.get(timeout=5)
                await incoming_message.ack()
                return incoming_message.body
            except QueueEmpty:
                return None
