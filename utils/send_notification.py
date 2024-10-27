import asyncio
from datetime import datetime
from data.NotesBotDB import getNotification, deleteNotification, getUserTimezone
import pytz

async def sendNotification(bot):

    while True:
        data = await getNotification()

        for n in data:
            if n[2]:
                user_timezone = pytz.timezone(await getUserTimezone(n[0]))
                utc_now = datetime.now(pytz.utc)
                user_time = utc_now.astimezone(user_timezone)
                print(user_time)
                print(data)
                
                try:
                    datetime.strptime(n[2], '%Y-%m-%d %H:%M')
                except ValueError:
                    notification_time = datetime.strptime(n[2], '%H:%M')
                    if notification_time.hour == user_time.hour and notification_time.minute == user_time.minute:
                        await bot.send_message(n[0], f"Notification! <b>{n[1]}</b>")
                        await deleteNotification(n[0], n[1])
                else:
                    notification_time = datetime.strptime(n[2], '%Y-%m-%d %H:%M')
                    if notification_time.date() == user_time.date():
                        if notification_time.hour == user_time.hour and notification_time.minute == user_time.minute:
                            await bot.send_message(n[0], f"Notification! <b>{n[1]}</b>")
                            await deleteNotification(n[0], n[1])
        await asyncio.sleep(60)
    