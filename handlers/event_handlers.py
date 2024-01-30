""" Module for different events router  """
from typing import Any
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, MessageReactionUpdated

router = Router()


@router.message(Command("chat_description", ignore_case=True))
async def set_chat_description(message: Message, command: CommandObject) -> None:
    """function to change chat name info"""
    chat_description = command.args
    await message.bot.set_my_short_description(chat_description)


@router.message_reaction()
async def message_reaction_handler(mru: MessageReactionUpdated) -> Any:
    """function which handles message reaction event"""
    print("Message Reaction!")


@router.edited_message()
async def edited_message_handler(message: Message) -> Any:
    """function which handles message editing event"""
    await message.reply(text="Edited the message!!!")


@router.message(Command("delete100", prefix='%'))
async def delete100(message: Message) -> None:
    """function to clear last 100 chat messages"""
    last_id = message.message_id
    result: bool = await message.bot.delete_messages(
        message.chat.id, list(range(last_id - 100, last_id))
    )
    print("Chat history cleared the last 100 messages but not older then 48 hours... operation succeeded : {0}".format(
        str(result)))
