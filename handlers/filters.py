""" Module for different types messages router  """
import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.formatting import (
    as_list, as_marked_section, Bold, as_key_value, HashTag
)

from keyboards.kb_questions import kb_yes_no

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.content_type.in_({'sticker', 'photo'}))
async def message_with_sticker(message: Message):
    """function for sticker or photo messages"""
    await message.answer("It is a sticker!")


@router.message(F.animation)
async def message_with_gif(message: Message):
    """function for GIF animation messages"""
    await message.answer("It is GIF! - Graphic Interchange Format")
    await message.reply_animation(message.animation.file_id)


@router.message(Command("job"))
async def cmd_start(message: Message):
    """job command handler function"""
    await message.answer("Do you like your job?", reply_markup=kb_yes_no())


@router.message(F.text.lower() == "yes")
async def answer_yes(message: Message):
    """yes answer function"""
    await message.answer("Nice to hear that!", reply_markup=ReplyKeyboardRemove())


@router.message(F.text.lower() == "no")
async def answer_no(message: Message):
    """no answer function"""
    await message.answer("Sorry...", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Yes, download & convert.")
async def answer_yes(message: Message):
    """yes download & convert answer function"""
    await message.answer("Nice to hear that!", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "No, thanks.")
async def answer_no(message: Message):
    """no answer function"""
    await message.answer("Ok, no problem :)", reply_markup=ReplyKeyboardRemove())


@router.message(F.text.lower() == "both")
async def answer_sqlite(message: Message):
    """sqlite answer function"""
    await message.answer(
        "Oh, I like your answer!\n <b><em>There is no bad weather it's only bad clothes</em></b>",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(F.text.lower() == "winter")
async def answer_postgresql(message: Message):
    """postgresql answer function"""
    await message.answer(
        "Oh, you like cold weather :) ...",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(F.text.lower() == "summer")
async def answer_postgresql(message: Message):
    """postgresql answer function"""
    await message.answer(
        "Oh, you don't like cold... you like warm weather... :)",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(F.text)
async def message_with_text(message: Message):
    """function for echo text messages keeping initial formatting"""
    time_now = datetime.now().strftime('%H:%M')
    logger.info(f"Unknown command on {time_now} or a simple text message: {message.html_text} :)")
    await message.answer(f"Unknown command on {time_now} or a simple text message: {message.html_text} :)")
