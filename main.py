import asyncio
import time
from src.broker.service import BrokerService
from src.password.service import PasswordEmailService
from src.settings.settings import settings
from src.smtp.service import SMTPEmailService


async def send():
    sender = SMTPEmailService(broker=BrokerService(broker_url=settings.broker_settings.broker_full_url))
    await sender.send_message()


async def send_verify_code():
    sender = PasswordEmailService(broker=BrokerService(broker_url=settings.broker_settings.broker_full_url))
    await sender.send_password_change_code()

while True:
    asyncio.run(send())
    asyncio.run(send_verify_code())
    time.sleep(10)
