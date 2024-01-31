""" AI module """
import logging
from os import getenv
import openai

from aiogram import types, Router
from aiogram.filters import Command
from main import bot

router = Router()
logger = logging.getLogger(__name__)


class Reference:
    """A class to store the previous response from Chat GPT API."""

    def __init__(self) -> None:
        self.response = ""


reference = Reference()

openai.api_key = getenv("OPEN_AI_API")
MODEL_NAME = getenv("MODEL_NAME")


def clear_past():
    """A function to clear the past conversations."""
    reference.response = ""


@router.message(Command("ai"))
async def chatgpt(msg: types.Message):
    """A handler to process user's input and generate a response using ChatGPT API"""
    logger.info("...ai chat GPT3.5 command triggered")
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "assistant", "content": reference.response},
            {"role": "user", "content": msg.text},
        ],
    )
    reference.response = response["choices"][0]["message"]["content"]
    await bot.send_message(chat_id=msg.chat.id, text=f"{reference.response}")
