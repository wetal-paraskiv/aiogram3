import functools
import logging

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, ReplyKeyboardRemove
from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from main import bot
from keyboards.kb_questions import kb_timer_interval
from utils.util import Util

router = Router()
scheduler = AsyncIOScheduler()
util = Util()
logger = logging.getLogger(__name__)


async def timer_message(chat_id, topic) -> None:
    """Scheduler for reminding something..."""
    if util.is_daytime():
        await bot.send_message(chat_id=chat_id, text=f"Reminder: ...{topic}...")


@router.message(Command("remind", ignore_case=True))
async def get_timer_args(message: Message, command: CommandObject):
    """function to get timer topic and timer interval for reminding something..."""
    if command.args is None:
        await message.answer("Please provide reminder topic!")
        return
    await message.reply(text="Choose reminder interval", reply_markup=kb_timer_interval(command.args))


@router.message(Command("set_timer", ignore_case=True))
async def scheduler_add_job(message: Message, command: CommandObject):
    """Scheduler for reminding something..."""
    logger.info("...set_timer function")
    data = command.args.split(' ')
    interval = data[0]
    topic_list = data[1:]
    topic = ' '.join(topic_list)
    reminder_id = topic + str(message.from_user.id)
    await message.answer(text=f"{topic.capitalize()} reminder, timer interval: {interval}",
                         reply_markup=ReplyKeyboardRemove())
    scheduler.add_job(functools.partial(timer_message, chat_id=message.chat.id, topic=topic),
                      'interval',
                      seconds=int(interval),
                      id=reminder_id)
    if scheduler.state == 0:
        scheduler.start()
    logger.info(f"'{topic}' job added to scheduler with interval: {interval}")
    return


@router.message(Command("stop", ignore_case=True))
async def schedule_remove_job(message: Message, command: CommandObject):
    """Scheduler remove job function..."""
    logger.info("...stop command...")
    if command.args is None:
        await message.answer("To stop reminder please provide topic!")
        return

    job_id = command.args + str(message.from_user.id)
    try:
        scheduler.remove_job(job_id=job_id)
        logging.info(f"Scheduler removed reminder (id: {job_id})")
        await message.answer(f"Reminder {command.args} was removed!")
    except JobLookupError:
        await message.answer(f"Reminder with topic: {command.args} was not found!")
    return
