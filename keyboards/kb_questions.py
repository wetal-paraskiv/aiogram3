""""Module for bot keyboards"""

from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_yes_no() -> ReplyKeyboardMarkup:
    """yes, no keyboard function"""
    kb = ReplyKeyboardBuilder()
    kb.button(text="Yes")
    kb.button(text="No")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def kb_start_question() -> ReplyKeyboardMarkup:
    """yes, no keyboard function"""
    kb = [
        [
            types.KeyboardButton(text="Both"),
            types.KeyboardButton(text="Winter"),
            types.KeyboardButton(text="Summer"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        is_persistent=True,
        resize_keyboard=True,
        input_field_placeholder="Choose preferred answer...",
    )
    return keyboard
