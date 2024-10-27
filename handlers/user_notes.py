from datetime import datetime
from aiogram import F, Router
from aiogram.types import Message
import pytz
from keyboards import reply, builders
from data.NotesBotDB import selectNotesDB, selectNoteDB, deleteNoteDB, editNoteDB, getUserTimezone, setUserTimezone
from utils.states import notesCommands
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

router = Router()

#меню со всеми нотатками юзера
@router.message(StateFilter(None), F.text.lower() == 'my notes')
async def selectNotes(message: Message, state: FSMContext):
    notes = await selectNotesDB(message.from_user.id)
    await message.answer('These are your notes', reply_markup=builders.notesKb(notes))
    await state.set_state(notesCommands.myNotesState)
    await state.update_data(myNotesState=notes)

#отдельная нотатка
@router.message(notesCommands.myNotesState, F.text)
async def Note(message: Message, state: FSMContext):
    if message.text == '❌':
        await message.answer('Returning...', reply_markup=reply.main_kb)
        await state.clear()
    else:
        try:
            data = await selectNoteDB(message.from_user.id, message.text)
            await message.answer(data[0], reply_markup=reply.note_kb)
            await message.answer(data[1])
            if data[2]:
                await message.answer(data[2])
            await state.set_state(notesCommands.myNoteState)
            await state.update_data(myNoteState=data[0])
        except TypeError: 
            await message.answer('пошел нахуй, нет такой')

#действия с нотаткой
@router.message(notesCommands.myNoteState, F.text)
async def deleteEditNote(message: Message, state: FSMContext):
    if message.text == '❌':
        data = await state.get_data()
        await message.answer('Returning...', reply_markup=builders.notesKb(data['myNotesState']))
        await state.set_state(notesCommands.myNotesState)

    elif message.text.lower() == 'delete note':
        data = await state.get_data()
        await deleteNoteDB(message.from_user.id, data['myNoteState'])
        await message.answer('Note deleted successfully', reply_markup=reply.main_kb)
        await state.clear()

    elif message.text.lower() == 'edit note':
        await message.answer('What do you want to edit?', reply_markup=reply.edit_kb)
        await state.set_state(notesCommands.editNoteState)

#выбор что редактировать в нотатке
@router.message(notesCommands.editNoteState, F.text)
async def editNote(message: Message, state: FSMContext):
    if message.text == '❌':
        await message.answer('Returning...', reply_markup=reply.note_kb)
        await state.set_state(notesCommands.myNoteState)
    elif message.text.lower() == 'edit note name':
        await message.answer('Enter new note name', reply_markup=reply.cancel_kb)
        await state.set_state(notesCommands.editNoteNameState)

    elif message.text.lower() == 'edit note description':
        await message.answer('Enter new note description', reply_markup=reply.cancel_kb)
        await state.set_state(notesCommands.editNoteDescriptionState)

    elif message.text.lower() == 'edit note notification time':
        if await getUserTimezone(message.from_user.id):
            await message.answer('Enter new note notification time in full format or just hours and minutes. For example:', reply_markup=reply.cancel_kb)
            await message.answer('2024-10-13 17:44')
            await message.answer('17:44')
            await state.set_state(notesCommands.editNoteNotificationState)
        else:
            await message.answer('To receive notifications correctly, you need to set the time zone. First, select a continent', reply_markup=reply.timezone_continent_kb)
            await state.set_state(notesCommands.editTimezoneContinentState)

#редактирование имени
@router.message(notesCommands.editNoteNameState, F.text)
async def editNoteName(message: Message, state: FSMContext):
    if message.text == '❌':
        await message.answer('Returning...', reply_markup=reply.note_kb)
        await state.set_state(notesCommands.myNoteState)
    else:
        data = await state.get_data()
        await editNoteDB(user_id=message.from_user.id, note_text=data['myNoteState'], new_note_text=message.text)
        await message.answer('Note name edited successfully', reply_markup=reply.note_kb)
        await state.set_state(notesCommands.myNoteState)
        await state.update_data(myNoteState=message.text)
        await state.update_data(myNotesState=await selectNotesDB(message.from_user.id))

#редактирование описания
@router.message(notesCommands.editNoteDescriptionState, F.text)
async def editNoteDescription(message: Message, state: FSMContext):
    if message.text == '❌':
        await message.answer('Returning...', reply_markup=reply.note_kb)
        await state.set_state(notesCommands.myNoteState)
    else:
        data = await state.get_data()
        await editNoteDB(user_id=message.from_user.id, note_text=data['myNoteState'], new_note_description=message.text)
        await message.answer('Note description edited successfully', reply_markup=reply.note_kb)
        await state.set_state(notesCommands.myNoteState)

#редактирование оповещения
@router.message(notesCommands.editNoteNotificationState, F.text)
async def editNoteNotification(message: Message, state: FSMContext):
    if message.text == '❌':
        await message.answer('Returning...', reply_markup=reply.note_kb)
        await state.set_state(notesCommands.myNoteState)
    else:
        try: 
            datetime.strptime(message.text, '%Y-%m-%d %H:%M')
        except ValueError:
            try: 
                datetime.strptime(message.text, '%H:%M')
            except ValueError:
                await message.answer('Please enter correct notification time')
            else:
                data = await state.get_data()
                await editNoteDB(user_id=message.from_user.id, note_text=data['myNoteState'], new_note_notification=message.text)
                await message.answer('Note notification time edited successfully', reply_markup=reply.note_kb)
                await state.set_state(notesCommands.myNoteState)
        else:
            data = await state.get_data()
            await editNoteDB(user_id=message.from_user.id, note_text=data['myNoteState'], new_note_notification=message.text)
            await message.answer('Note notification time edited successfully', reply_markup=reply.note_kb)
            await state.set_state(notesCommands.myNoteState)

#редактирование часового пояса (выбор континента)
@router.message(notesCommands.editTimezoneContinentState, F.text)
async def editTimezoneContinent(message: Message, state: FSMContext):
    await message.answer('Now select a city', reply_markup=builders.timezoneCityKb(message.text))
    await state.set_state(notesCommands.editTimezoneCityState)

#редактирование часового пояса (выбор города и сохранение)
@router.message(notesCommands.editTimezoneCityState, F.text)
async def editTimezoneCity(message: Message, state: FSMContext):
    try: 
        pytz.timezone(message.text)
    except pytz.exceptions.UnknownTimeZoneError:
        await state.set_state(notesCommands.editTimezoneContinentState)
        await message.answer('Wrong information, try again', reply_markup=reply.timezone_continent_kb)
    else:
        await setUserTimezone(message.from_user.id, message.text)
        await message.answer('Timezone selected successfully', reply_markup=reply.main_kb)
        await state.clear()

#редактирование часового пояса из меню
@router.message(StateFilter(None), F.text.lower() == "change timezone")
async def changeTimezone(message: Message, state: FSMContext):
        timezone = await getUserTimezone(message.from_user.id)
        if timezone:
            await message.answer(f'Your current timezone: {timezone}')
        await message.answer('To receive notifications correctly, you need to set the time zone. First, select a continent', reply_markup=reply.timezone_continent_kb)
        await state.set_state(notesCommands.editTimezoneContinentState)
    

@router.message(F.text)
async def echo(message: Message):
    await message.answer("Понял принял")
