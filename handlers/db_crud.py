"""Module providing postgres database connection & orm methods to support bot commands."""
import logging

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.engine import engine as postgres_engine
from models.note import Note
from utils.enums import BotMessage

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("help", ignore_case=True))
async def help_(message: Message) -> None:
    """/help Function to list available bot commands"""
    logger.info(" help command")
    await message.answer(text=BotMessage.HELP, parse_mode="HTML")


@router.message(Command("add", ignore_case=True))
async def add(message: Message, command: CommandObject) -> None:
    """ "Function to add a new note"""
    data = command.args
    note = Note(data, str(message.from_user.id))
    with Session(postgres_engine) as session:
        session.add(note)
        session.commit()
    logger.info("...add command")
    await message.answer(text=BotMessage.ADD)


@router.message(Command("list", ignore_case=True))
async def get_all(message: Message) -> None:
    """Function to list all registered notes"""
    logger.info("...list command")
    notes = ""
    await message.answer(text=BotMessage.ALL_NOTES)
    session = Session(postgres_engine)
    result_set = select(Note).where(Note.user_id == str(message.from_user.id))
    for note in session.scalars(result_set):
        notes += str(note.id) + ". " + note.note + "\n"
    if notes == "":
        await message.answer(text=BotMessage.EMPTY_LIST)
    else:
        await message.answer(text=notes)


@router.message(Command("del", ignore_case=True))
async def delete(message: Message, command: CommandObject) -> None:
    """ Function to delete a note."""
    logger.info("...del command")
    note_id = command.args
    stmt = select(Note).where(Note.id == int(note_id)).where(Note.user_id == str(message.from_user.id))
    with Session(postgres_engine) as session:
        try:
            note = session.scalars(stmt).one()
            await message.answer(text=BotMessage.DELETE + note_id + ". " + note.note)
            session.delete(note)
            session.commit()
        except NoResultFound as e:
            session.rollback()
            await message.answer(text=BotMessage.NO_NOTES_BY_ID + note_id + "... ")
            logger.warning(e)


@router.message(Command("clear", ignore_case=True, prefix='/'))
async def delete_all(message: Message, command: CommandObject) -> None:
    """ "Function to delete all notes."""
    logger.info("cleared all notes, name: " + message.from_user.full_name)
    code = command.args
    if code == "all":
        with Session(postgres_engine) as session:
            session.query(Note).where(Note.user_id == str(message.from_user.id)).delete()
            session.commit()
        await message.answer(text=BotMessage.TRUNCATE)
    else:
        await message.answer(text=BotMessage.CODE)
