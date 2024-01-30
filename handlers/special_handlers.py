from random import randint

from aiogram import types, html, F, Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.formatting import Text
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

router = Router()


@router.message(Command("extract"))
async def extract_data(message: Message) -> None:
    data = {"URL": "<N/A>", "email": "<N/A>", "code": "<N/A>"}
    entities = message.entities or []
    for item in entities:
        if item.type in data.keys():
            data[item.type] = item.extract_from(message.text)
    await message.reply("That's what I found:\n"
                        f"URL: {html.quote(data['URL'])}\n"
                        f"email: {html.quote(data['email'])}\n"
                        f"code: {html.quote(data['code'])}\n")


@router.message(Command("set_timer", prefix='%'))  # can add more prefixes
async def set_timer_message(message: Message, command: CommandObject):
    if command.args is None:
        await message.answer("command /set_timer error: no args for time & message provided!")
        return
    try:
        delay_time, text_to_send = command.args.split(' ', maxsplit=1)
    except ValueError:
        content = Text("Wrong format!\nCorrect format: /set_timer <time> <message>")
        await message.answer(**content.as_kwargs())
        return
    await message.answer(
        "Timer added!\n"
        f"delay-time: {delay_time}\n"
        f"message: {text_to_send}")


@router.message(F.new_chat_members)
async def somebody_added(message: Message):
    for user in message.new_chat_members:
        await message.reply(f"Salut, {user.full_name}")


@router.message(F.user_shared)
async def on_user_shared(message: types.Message):
    print(
        f"Request {message.user_shared.request_id}. "
        f"User ID: {message.user_shared.user_id}"
    )


@router.message(F.chat_shared)
async def on_chat_shared(message: types.Message):
    print(
        f"Request {message.chat_shared.request_id}. "
        f"User ID: {message.chat_shared.chat_id}"
    )


@router.message(F.request_contact)
async def on_request_contact(message: types.Message):
    print(
        f"FullName {message.from_user.full_name}. "
        f"User ID: {message.from_user.get_profile_photos()}"
    )


@router.message(Command("special_buttons"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Geolocation request", request_location=True),
        types.KeyboardButton(text="Request contacts", request_contact=True))
    builder.row(
        types.KeyboardButton(
            text="Создать викторину",
            request_poll=types.KeyboardButtonPollType(type="quiz"))
    )
    builder.row(
        types.KeyboardButton(
            text="Выбрать премиум пользователя",
            request_user=types.KeyboardButtonRequestUser(
                request_id=1,
                user_is_premium=True
            )
        ),
        types.KeyboardButton(
            text="Выбрать супергруппу с форумами",
            request_chat=types.KeyboardButtonRequestChat(
                request_id=2,
                chat_is_channel=False,
                chat_is_forum=True
            )
        )
    )
    await message.answer(
        "Choose action:", reply_markup=builder.as_markup(resize_keyboard=True), )


@router.message(Command("inline_url", prefix='%'))
async def cmd_inline_url(message: types.Message, bot: Bot):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="GitHub", url="https://github.com")
    )
    builder.row(types.InlineKeyboardButton(
        text="Telegram official channel",
        url="tg://resolve?domain=telegram")
    )
    # To show ID button, user must have has_private_forwards False
    user_id = message.from_user.id
    chat_info = await bot.get_chat(user_id)
    if not chat_info.has_private_forwards:
        builder.row(types.InlineKeyboardButton(
            text="Some user...",
            url=f"tg://user?id={user_id}")
        )
    await message.answer(
        'Choose link',
        reply_markup=builder.as_markup(),
    )


@router.message(Command("random"))
async def cmd_random_number(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='Push me', callback_data='random_number'))
    await message.answer('Push button to get a random number between 1 - 10', reply_markup=builder.as_markup())


@router.callback_query(F.data == 'random_number')
async def send_random_number(callback: types.CallbackQuery):
    await callback.message.answer(str(randint(1, 100)))
    await callback.answer(text="Thanks for using notesBot!", show_alert=True)
