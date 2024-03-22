import aio_pika
from aio_pika.exceptions import QueueEmpty
from src.settings.settings import settings


async def get_user_email_from_broker():
    """Получить данные из RabbitMQ"""
    connection = await aio_pika.connect_robust(url=settings.broker_settings.broker_full_url)

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
