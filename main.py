import asyncio
import time
from src.smtp.service import send_message, send_password_change_code


async def send():
    await send_message()


async def send_verify_code():
    await send_password_change_code()

while True:
    asyncio.run(send())
    asyncio.run(send_verify_code())
    time.sleep(10)
