import sqlite3
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, StateFilter
from keyboards import reply
from data.NotesBotDB import addUserDB, addNoteDB
from utils.states import notesCommands
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(f"Hello <b>{message.from_user.first_name}</b>! I'm Notes Bot, you can save your notes here.", reply_markup=reply.main_kb)
    await addUserDB(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    await state.clear()


@router.message(StateFilter(None), F.text.lower() == 'add note')
async def addNote(message: Message, state: FSMContext):
    await message.answer('Enter your note')
    await state.set_state(notesCommands.addNoteNameState)

@router.message(notesCommands.addNoteNameState, F.text)
async def addNote2(message: Message, state: FSMContext):
    await message.answer('Now enter a description for the note')
    await state.update_data(addNoteNameState=message.text)
    await state.set_state(notesCommands.addNoteDescriptionState)

@router.message(notesCommands.addNoteDescriptionState, F.text)
async def addNote2(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        await addNoteDB(message.from_user.id, data['addNoteNameState'], message.text)
        await message.answer('Note added successfully')
    except sqlite3.IntegrityError:
        await message.answer('You\'re already have note with this name')
    await state.set_state()
