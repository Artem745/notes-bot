import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.client.bot import DefaultBotProperties
from handlers.user_notes import router as user_notes_router
from handlers.add_notes import router as add_notes_router
from utils.send_notification import sendNotification

bot = Bot(
    token="7873037537:AAGHd8heG6JKdW3lcYb7oSsi7_VDxT_3VPc",
    default=DefaultBotProperties(parse_mode="HTML"),
)
dp = Dispatcher()


async def main():
    dp.include_routers(add_notes_router, user_notes_router)

    asyncio.create_task(sendNotification(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
