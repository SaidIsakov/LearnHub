import telegram
import asyncio
from decouple import config


BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')


async def _send_message(chat_id: str, text: str) -> None:
  """Отправляет сообщение в Telegram"""
  bot = telegram.Bot(token=config('TELEGRAM_BOT_TOKEN'))
  await bot.send_message(chat_id=chat_id, text=text)


def send_message(chat_id: str, text: str) -> None:
  """Синхронная обёртка для отправки сообщения"""
  asyncio.run(_send_message(chat_id, text))
