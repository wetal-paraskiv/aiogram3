""" Module for different events router  """
import logging
from typing import Any
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, MessageReactionUpdated

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("chat_description", ignore_case=True))
async def set_chat_description(message: Message, command: CommandObject) -> None:
    """function to change chat name info"""
    chat_description = command.args
    await message.bot.set_my_short_description(chat_description)


@router.message_reaction()
async def message_reaction_handler(mru: MessageReactionUpdated) -> Any:
    """function which handles message reaction event"""
    logger.info("Message Reaction!")


@router.edited_message()
async def edited_message_handler(message: Message) -> Any:
    """function which handles message editing event"""
    await message.reply(text="Edited the message!!!")
