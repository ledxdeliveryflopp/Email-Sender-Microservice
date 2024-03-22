import asyncio
import time
from src.smtp.service import send_message


async def send():
    await send_message()


while True:
    asyncio.run(send())
    time.sleep(10)
