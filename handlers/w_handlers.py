import functools

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import bot

router = Router()
scheduler = AsyncIOScheduler()


async def water_message(chat_id) -> None:
    """Scheduler for reminding something..."""
    print("Reminder: Don't forget about Water...")
    await bot.send_message(chat_id=chat_id, text='Reminder: don\'t forget about Water...')


@router.message(Command("water", ignore_case=True))
async def schedule_add_job(message: Message, command: CommandObject):
    """Scheduler for reminding something..."""
    if command.args is None or not command.args.isdigit():
        await message.answer("Please provide the periodicity for reminder!")
        return
    else:
        interval = int(command.args)
        scheduler.add_job(functools.partial(water_message, chat_id=message.chat.id),
                          'interval',
                          seconds=interval,
                          id='water_reminder' + str(message.from_user.id))
        if scheduler.state == 0:
            scheduler.start()
        print("Water message job added to scheduler!")
        return


@router.message(Command("water_stop", ignore_case=True))
async def schedule_remove_job(message: Message):
    """Scheduler remove job function..."""
    scheduler.remove_job(job_id='water_reminder' + str(message.from_user.id))
    print("Scheduler removed the job with id: water_reminder" + str(message.from_user.id))
    await message.answer("Water reminder was removed!")
