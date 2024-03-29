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


def kb_download_convert(video_id) -> ReplyKeyboardMarkup:
    """yes, no video download keyboard function"""
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text=f"/ConvertVideo {video_id}", ))
    builder.add(types.KeyboardButton(text=f"No, thanks."))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


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


def kb_timer_interval(topic) -> ReplyKeyboardMarkup:
    """select time interval keyboard function"""
    builder = ReplyKeyboardBuilder()
    for i in range(15, 181, 15):
        builder.add(types.KeyboardButton(text=f"/set_timer {i} {topic}"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
