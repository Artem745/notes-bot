from aiogram.fsm.state import StatesGroup, State


class notesCommands(StatesGroup):
    addNoteNameState = State()
    addNoteDescriptionState = State()

    myNotesState = State()
    myNoteState = State()

    editNoteState = State()

    editNoteNameState = State()
    editNoteDescriptionState = State()

    editTimezoneContinentState = State()
    editTimezoneCityState = State()

    editNoteNotificationState = State()
