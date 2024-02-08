import logging
import time

from aiogram import Router, html
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.formatting import Text, Bold
from aiogram.utils.markdown import hbold

from handlers import ai_gpt, youtube_, events, special, reminder, filters, db_crud
from keyboards.kb_questions import kb_start_question

router = Router()

router.include_routers(
    ai_gpt.router,
    db_crud.router,
    youtube_.router,
    reminder.router,
    events.router,
    special.router,
    filters.router,
)

logger = logging.getLogger(__name__)


@router.message(Command("start", ignore_case=True))
async def start_(message: Message):
    """/start command function ..."""
    logger.info("...start command triggered...")
    username = message.from_user.full_name

    # # simple answer but with problems if the text contain '<User777>'
    # await message.answer(f"Hello, {hbold(username)}!")
    #
    # # This instrument works on top of Message entities instead of using HTML or Markdown markups
    # await message.answer(
    #     f"Hello, {html.bold(html.quote(username))}",
    #     parse_mode=ParseMode.HTML
    # )

    content = Text("Hello, ", Bold(username))
    await message.answer(**content.as_kwargs())
    time.sleep(1)

    await message.reply(
        "Are you a Winter or a Summer person ?", reply_markup=kb_start_question()
    )
